import pytest
from actstream import action
from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.sites import models as site_models
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from model_bakery import baker
from notifications.signals import notify
from pytest_django.asserts import assertContains, assertNotContains

from recoco import verbs
from recoco.apps.home import models as home_models
from recoco.apps.projects import models as project_models
from recoco.utils import login


@pytest.mark.django_db
def test_site_dashboard_not_available_for_non_staff_users(client):
    url = reverse("crm-site-dashboard")
    with login(client):
        response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_site_dashboard__shows_project_actions_to_staff(request, client):
    site = get_current_site(request)
    project = baker.make(project_models.Project, sites=[site])
    action.send(project, verb="Was here", target=project)

    other_site = baker.make(site_models.Site)
    with settings.SITE_ID.override(other_site.pk):
        other = baker.make(project_models.Project, sites=[other_site])
        action.send(other, verb="Was not here", target=other)

    url = reverse("crm-site-dashboard")
    with login(client, groups=["example_com_staff"]):
        response = client.get(url)

    assert response.status_code == 200

    assertContains(response, "Was here")
    assertNotContains(response, "Was not here")


@pytest.mark.django_db
def test_site_dashboard_hides_other_site_project_notifications(request, client):
    user = baker.make(auth_models.User)

    other_site = baker.make(site_models.Site)
    with settings.SITE_ID.override(other_site.pk):
        other_project = baker.make(project_models.Project, sites=[other_site])
        # a notification for this project
        verb = verbs.CRM.NOTE_CREATED
        notify.send(
            sender=user,
            recipient=user,
            verb=verb,
            action_object=other_project,
            target=other_project,
            public=False,  # only appear on crm stream
        )

    url = reverse("crm-site-dashboard")
    with login(client, user=user, groups=["example_com_staff"]):
        response = client.get(url)

    assert response.status_code == 200

    assertNotContains(response, verb)


# -- Site configuration
@pytest.mark.django_db
def test_site_configuration_not_available_for_non_admin_users(request, client):
    site = get_current_site(request)
    baker.make(home_models.SiteConfiguration, site=site)

    url = reverse("crm-site-configuration")

    with login(client):
        response = client.get(url)
    assert response.status_code == 403


# -- Site configuration
@pytest.mark.django_db
def test_site_configuration_not_available_for_staff_users(request, client):
    site = get_current_site(request)
    baker.make(home_models.SiteConfiguration, site=site)
    user = baker.make(auth_models.User)

    url = reverse("crm-site-configuration")

    with login(client, user=user, groups=["example_com_staff"]):
        from recoco.utils import has_perm

        print(has_perm(user, "sites.manage_configuration", site))

        response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_site_configuration_available_for_admin_users(request, client):
    site = get_current_site(request)
    baker.make(home_models.SiteConfiguration, site=site)
    user = baker.make(auth_models.User)

    url = reverse("crm-site-configuration")
    with login(client, user=user, groups=["example_com_admin"]):
        response = client.get(url)
    assert response.status_code == 200


# eof
