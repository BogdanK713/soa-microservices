// calendar-service/graphql/schema.js
// GraphQL schema + resolvers for Google Calendar
// Requires env: GOOGLE_SERVICE_ACCOUNT_EMAIL, GOOGLE_PRIVATE_KEY, CALENDAR_ID (default)

const { GraphQLScalarType, Kind } = require("graphql");
const { google } = require("googleapis");

// ---- helpers: Google auth + Calendar client ----
function getGoogleCalendar() {
  const email = process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL;
  let key = process.env.GOOGLE_PRIVATE_KEY || "";

  if (!email || !key) {
    throw new Error(
      "Missing GOOGLE_SERVICE_ACCOUNT_EMAIL or GOOGLE_PRIVATE_KEY env variables."
    );
  }
  // keys often come with \n escaped in .env files
  key = key.replace(/\\n/g, "\n");

  const auth = new google.auth.JWT({
    email,
    key,
    scopes: ["https://www.googleapis.com/auth/calendar.readonly"],
  });

  return google.calendar({ version: "v3", auth });
}

// ---- GraphQL scalar for ISO DateTime ----
const DateTime = new GraphQLScalarType({
  name: "DateTime",
  description: "ISO-8601 date-time string",
  serialize(value) {
    // value sent to the client
    return new Date(value).toISOString();
  },
  parseValue(value) {
    // value from the client variables
    // we keep it as a string and pass to Google API
    return value;
  },
  parseLiteral(ast) {
    if (ast.kind === Kind.STRING) return ast.value;
    return null;
  },
});

// ---- typeDefs ----
const typeDefs = `#graphql
  scalar DateTime

  type Attendee {
    email: String
    displayName: String
    responseStatus: String
  }

  type Event {
    id: ID!
    summary: String
    description: String
    location: String
    htmlLink: String
    start: DateTime
    end: DateTime
    attendees: [Attendee!]
  }

  type Calendar {
    id: ID!
    summary: String
    description: String
    timeZone: String
  }

  type Query {
    # list calendars the service account can see
    calendars: [Calendar!]!

    # list events from a calendar; all args optional
    events(
      calendarId: ID
      timeMin: DateTime
      timeMax: DateTime
      maxResults: Int
    ): [Event!]!

    # get single event by id
    event(calendarId: ID, eventId: ID!): Event
  }
`;

// ---- resolvers ----
const resolvers = {
  DateTime,

  Query: {
    async calendars() {
      const calendar = getGoogleCalendar();
      const res = await calendar.calendarList.list();
      const items = res.data.items || [];
      return items.map((c) => ({
        id: c.id,
        summary: c.summary || null,
        description: c.description || null,
        timeZone: c.timeZone || null,
      }));
    },

    async events(_, args) {
      const calendar = getGoogleCalendar();
      const calendarId = args.calendarId || process.env.CALENDAR_ID;
      if (!calendarId) {
        throw new Error("calendarId is required (or set CALENDAR_ID env).");
      }

      const now = new Date();
      const in30 = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000);

      const res = await calendar.events.list({
        calendarId,
        timeMin: args.timeMin || now.toISOString(),
        timeMax: args.timeMax || in30.toISOString(),
        singleEvents: true,
        orderBy: "startTime",
        maxResults: args.maxResults || 50,
      });

      const items = res.data.items || [];
      return items.map((e) => ({
        id: e.id,
        summary: e.summary || null,
        description: e.description || null,
        location: e.location || null,
        htmlLink: e.htmlLink || null,
        start: (e.start && (e.start.dateTime || e.start.date)) || null,
        end: (e.end && (e.end.dateTime || e.end.date)) || null,
        attendees: (e.attendees || []).map((a) => ({
          email: a.email || null,
          displayName: a.displayName || null,
          responseStatus: a.responseStatus || null,
        })),
      }));
    },

    async event(_, { calendarId, eventId }) {
      const calendar = getGoogleCalendar();
      const cid = calendarId || process.env.CALENDAR_ID;
      if (!cid) throw new Error("calendarId is required (or set CALENDAR_ID).");
      if (!eventId) throw new Error("eventId is required.");

      const res = await calendar.events.get({ calendarId: cid, eventId });
      const e = res.data;
      return {
        id: e.id,
        summary: e.summary || null,
        description: e.description || null,
        location: e.location || null,
        htmlLink: e.htmlLink || null,
        start: (e.start && (e.start.dateTime || e.start.date)) || null,
        end: (e.end && (e.end.dateTime || e.end.date)) || null,
        attendees: (e.attendees || []).map((a) => ({
          email: a.email || null,
          displayName: a.displayName || null,
          responseStatus: a.responseStatus || null,
        })),
      };
    },
  },
};

module.exports = { typeDefs, resolvers };
