# encoding: utf-8

"""
Models for reminders

authors: raphael.marvie@beta.gouv.fr, guillaume.libersat@beta.gouv.fr
created: 2021-09-28 12:59:08 CEST
"""

import datetime
import logging

from django.utils import timezone
from urbanvitaliz.apps.tasks.models import Task

from . import models

logger = logging.getLogger("main")


def make_or_update_reminder(site, project, kind, deadline):
    if deadline < timezone.localdate():
        return None

    if site not in project.sites.all():
        return None

    existing_reminder = (
        models.Reminder.on_site_to_send.filter(project=project, kind=kind)
        .order_by("-deadline")
        .first()
    )

    task_count = (
        project.tasks.filter(status__in=Task.OPEN_STATUSES)
        .filter(site=site)
        .exclude(public=False)
        .count()
    )

    if (existing_reminder is None) and task_count == 0:
        return None

    if existing_reminder:
        # check if this reminder still makes sense ; i.e. we still have unattended
        # Recommendations to remind. Delete it otherwise
        if task_count == 0:
            logger.warning(
                f"Deleting bogus {kind} reminder since there are no more"
                f"open tasks for project <{project.name}>"
                f" ({project.pk})"
            )
            existing_reminder.delete()
            return None
        else:
            if existing_reminder.deadline != deadline:
                existing_reminder.deadline = deadline
                existing_reminder.save()
                logger.info(
                    f"Updating reminder <{existing_reminder.kind}> "
                    f"for project <{project.name}>(id={project.pk})"
                )
            return existing_reminder

    logger.info(
        f"Creating reminder <{kind}> for project <{project.name}> ({project.pk})"
    )
    return models.Reminder.objects.create(
        site=site,
        project=project,
        deadline=deadline,
        kind=kind,
        origin=models.Reminder.SYSTEM,
    )


def get_due_reminder_for_project(site, project, kind):
    """Return the current reminder (=not sent yet) for a given kind."""
    try:
        reminder = models.Reminder.on_site_to_send.get(
            project=project,
            site=site,
            kind=kind,
            deadline__lte=timezone.localdate(),  # today
        )
    except models.Reminder.DoesNotExist:
        return None

    if not reminder:
        logger.debug(f"No due <{kind}> reminder!")
        return None

    return reminder


#################################################################
# New Recommendations Reminder
#################################################################
def make_or_update_new_recommendations_reminder(site, project, interval_in_days=7 * 6):
    """Given a project, generate reminders for new recommendations that may have been
    missed by the council. Default interval is 6 weeks.
    """
    last_task = (
        project.tasks.filter(status__in=Task.OPEN_STATUSES)
        .filter(site=site)
        .exclude(public=False)
        .order_by("-created_on")
        .first()
    )

    if last_task:
        last_task_created_on = last_task.created_on
    else:
        last_task_created_on = timezone.now()

    interval = datetime.timedelta(days=interval_in_days)
    deadline = (last_task_created_on + interval).date()

    return make_or_update_reminder(
        site=site, project=project, kind=models.Reminder.NEW_RECO, deadline=deadline
    )


def get_due_new_recommendations_reminder_for_project(site, project):
    return get_due_reminder_for_project(site, project, kind=models.Reminder.NEW_RECO)


#################################################################
# What's up? Reminder
#################################################################


def make_or_update_whatsup_reminder(site, project):
    """Given a project, generate a whats up email to the project owner to try to get her
    attention back. Interval is configured by the SiteConfiguration model.
    """
    last_activity = project.last_members_activity_at

    if not last_activity:
        logger.warning(
            f"Bogus project <{project.name}>(id={project.id}), "
            "no last members activity, skipping"
        )
        return None

    # last_reminder = (
    #     models.Reminder.on_site_sent.filter(project=project)
    #     .order_by("-deadline")
    #     .first()
    # )

    # interval_state = 0
    # if last_reminder:
    #     interval_state = last_reminder.state + 1

    # FIXME(glibersat) Hardcoded: fetch real interval from SiteConfiguration
    interval = datetime.timedelta(days=6 * 7)

    deadline = (last_activity + interval).date()

    return make_or_update_reminder(
        site=site, project=project, kind=models.Reminder.WHATS_UP, deadline=deadline
    )


def get_due_whatsup_reminder_for_project(site, project):
    return get_due_reminder_for_project(site, project, kind=models.Reminder.WHATS_UP)


# eof
