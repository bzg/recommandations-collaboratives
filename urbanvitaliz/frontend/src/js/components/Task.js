import Alpine from 'alpinejs'

import { editTaskUrl, deleteTaskReminderUrl } from '../utils/api'
import { formatDate } from '../utils/date'
import { toArchiveTooltip } from '../utils/tooltip'
import { renderMarkdown } from '../utils/markdown'
import { gravatar_url } from '../utils/gravatar'
import { truncate } from '../utils/taskStatus'

export default function Task(currentTask) {
    return {
        currentTask: null,
        currentTaskId: null,
        toArchiveTooltip,
        currentTaskFollowups: null,
        currentTaskNotifications: null,
        editTaskUrl,
        renderMarkdown,
        formatDate,
        gravatar_url,
        deleteTaskReminderUrl,
        truncate,
        init() {
            this.currentTask = currentTask
        },
        handleOpenDeleteModal() {
            this.$dispatch('open-delete-modal', this.currentTask)
        },
        handleOpenPreviewModal() {	
            this.$store.previewModal.open(this.currentTask.id)	
        },
        async onSetTaskPublic(task, value) {
            task.isLoading = true
            await this.$store.tasksData.patchTask(task.id, { public: value });
            await this.$store.tasksView.updateViewWithTask(task.id)
            task.isLoading = false
        },
        async handleMove(direction, task, otherTask) {

            const taskToChange = this.$store.tasksView.findById(task.id)
            const otherTaskToChange = this.$store.tasksView.findById(otherTask.id)

            taskToChange.isLoading = true
            otherTaskToChange.isLoading = true

            if (direction === 'above') {
                await this.$store.tasksData.moveAbove(task, otherTask)
            } else if (direction === 'below') {
                await this.$store.tasksData.moveBelow(task, otherTask)
            }

            await this.$store.tasksView.updateViewWithTask(task.id)
            await this.$store.tasksView.updateViewWithTask(otherTask.id)

            taskToChange.isLoading = true
            otherTaskToChange.isLoading = true
        },
        formatDateDisplay(date) {
            return new Date(date).toLocaleDateString('fr-FR');
        },
        getTaskColor(task) {
            if (!task.public && task.content === '') {
                return '-orange'
            } else if (!task.public) {
                return '-yellow'
            } else {
                return '-grey-dark'
            }
        },
        getTaskMessageCountLabel(count) {
            return count > 1 ? `${count} messages` : `${count} message`
        },
        getTaskNewMessageCountLabel(count) {
            return count > 1 ? `(${count} nouveaux)` : `(${count} nouveau)`
        }
    }
}

Alpine.data("Task", Task)
