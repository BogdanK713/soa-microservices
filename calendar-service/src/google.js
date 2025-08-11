const fs = require('fs');
const { google } = require('googleapis');

function buildAuth() {
  // Preferiramo key fajl ako je zadan
  const keyPath = process.env.GOOGLE_APPLICATION_CREDENTIALS;
  if (keyPath && fs.existsSync(keyPath)) {
    return new google.auth.GoogleAuth({
      keyFile: keyPath,
      scopes: ['https://www.googleapis.com/auth/calendar'],
    });
  }

  // Fallback na email + private key iz ENV-a
  const email = process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL;
  let privateKey = process.env.GOOGLE_PRIVATE_KEY;

  if (!email || !privateKey) {
    throw new Error('Google Calendar auth nije podešen.');
  }

  privateKey = privateKey.replace(/\\n/g, '\n');

  return new google.auth.JWT({
    email,
    key: privateKey,
    scopes: ['https://www.googleapis.com/auth/calendar'],
  });
}

function getCalendarClient() {
  const auth = buildAuth();
  return google.calendar({ version: 'v3', auth });
}

const TZ = process.env.TIME_ZONE || 'UTC';
const toISO = (d) => new Date(d).toISOString();

async function listEvents({ timeMin, timeMax, maxResults = 50, q }) {
  const calendarId = process.env.CALENDAR_ID;
  if (!calendarId) throw new Error('Missing CALENDAR_ID');

  const calendar = getCalendarClient();
  const params = {
    calendarId,
    singleEvents: true,
    orderBy: 'startTime',
    maxResults,
    timeMin: timeMin ? toISO(timeMin) : new Date(Date.now() - 24 * 3600 * 1000).toISOString(),
    timeMax: timeMax ? toISO(timeMax) : new Date(Date.now() + 30 * 24 * 3600 * 1000).toISOString(),
    q,
  };

  const res = await calendar.events.list(params);
  return res.data.items || [];
}

async function createEvent({ summary, description, start, end, attendees = [] }) {
  const calendarId = process.env.CALENDAR_ID;
  if (!calendarId) throw new Error('Missing CALENDAR_ID');

  const calendar = getCalendarClient();

  const now = new Date();
  const startDate = start ? new Date(start) : now;
  const endDate = end ? new Date(end) : new Date(startDate.getTime() + 30 * 60000);

  if (isNaN(startDate) || isNaN(endDate) || endDate <= startDate) {
    throw new Error('Invalid start/end');
  }

  const event = {
    summary: summary || 'Reservation',
    description: description || '',
    start: { dateTime: startDate.toISOString(), timeZone: TZ },
    end: { dateTime: endDate.toISOString(), timeZone: TZ },
    attendees: (attendees || [])
      .filter((a) => a && a.email)
      .slice(0, 20)
      .map((a) => ({ email: a.email, displayName: a.name })),
  };

  const res = await calendar.events.insert({ calendarId, requestBody: event });
  return res.data;
}

async function deleteEvent(eventId) {
  const calendarId = process.env.CALENDAR_ID;
  if (!calendarId) throw new Error('Missing CALENDAR_ID');
  if (!eventId) throw new Error('Missing eventId');

  const calendar = getCalendarClient();
  await calendar.events.delete({ calendarId, eventId });
  return { ok: true };
}

module.exports = { listEvents, createEvent, deleteEvent };
