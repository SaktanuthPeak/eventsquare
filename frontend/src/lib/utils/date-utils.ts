export function formatDateTime(dateString: string) {
		const date = new Date(dateString);
		return date.toLocaleDateString('en-GB', {
			day: 'numeric',
			month: 'short',
			year: 'numeric',
			hour: '2-digit',
			minute: '2-digit',
		});
	}

export function formatDate(dateString: string) {
		const date = new Date(dateString);
		return date.toLocaleDateString('en-GB', {
			day: 'numeric',
			month: 'short',
			year: 'numeric',
			timeZone: 'UTC'
		});
	}