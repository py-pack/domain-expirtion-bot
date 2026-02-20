export function formatIsoDate(isoDate: string): string {
  const parsed = new Date(isoDate)

  if (Number.isNaN(parsed.getTime())) {
    return isoDate
  }

  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(parsed)
}
