/** Only allow same-origin relative paths as post-login redirects. */
export function safeRedirectPath(raw: unknown, fallback = '/user-start'): string {
  if (typeof raw !== 'string' || !raw.startsWith('/') || raw.startsWith('//')) {
    return fallback
  }
  return raw
}
