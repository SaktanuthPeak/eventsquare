export function formatAllowedDates(allowed_dates:any) {
		if (!allowed_dates) return 'No date information';

		const formatter = new Intl.DateTimeFormat('en-US', {
			year: 'numeric',
			month: 'short',
			day: 'numeric'
		});

		if (allowed_dates.date_range) {
			const start = new Date(allowed_dates.date_range.start_date);
			const end = new Date(allowed_dates.date_range.end_date);
			return `${formatter.format(start)} - ${formatter.format(end)}`;
		}

		if (allowed_dates.single_date) {
			return formatter.format(new Date(allowed_dates.single_date));
		}

		return 'No date information';
	}