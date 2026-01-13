export function formatDateTime(dateString: string) {
		const date = new Date(dateString);
		return date.toLocaleDateString('en-UK', {
			day: 'numeric',
			month: 'short',
			year: 'numeric',
			hour: '2-digit',
			minute: '2-digit'
		});
	}