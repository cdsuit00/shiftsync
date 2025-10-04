import { useEffect, useState, useContext } from "react";
import api from "../services/api";
import { AuthContext } from "../context/AuthContext";
import { Calendar, dateFnsLocalizer } from "react-big-calendar";
import { parseISO, format, startOfWeek, getDay } from "date-fns";
import enUS from "date-fns/locale/en-US";

const locales = { "en-US": enUS };
const localizer = dateFnsLocalizer({ format, parse: parseISO, startOfWeek: () => startOfWeek(new Date()), getDay, locales });

export default function ScheduleCalendar() {
  const { user } = useContext(AuthContext);
  const [events, setEvents] = useState([]);

  useEffect(() => {
    async function loadShifts() {
      try {
        const res = await api.get("/api/shifts");
        const evts = res.data.map((s) => ({
          id: s.id,
          title: s.title,
          start: new Date(s.start_time),
          end: new Date(s.end_time),
          resource: s,
        }));
        setEvents(evts);
      } catch (err) {
        alert("Failed to load shifts");
      }
    }
    loadShifts();
  }, []);

  // Manager: on event resize or drop we send update to backend
  const onEventDrop = async ({ event, start, end }) => {
    if (user.role !== "manager") return;
    try {
      await api.put(`/api/shifts/${event.id}`, {
        user_id: event.resource.user_id,
        title: event.title,
        start_time: start.toISOString(),
        end_time: end.toISOString(),
        notes: event.resource.notes,
      });
      setEvents((prev) => prev.map((e) => (e.id === event.id ? { ...e, start, end } : e)));
    } catch (err) {
      alert(err.response?.data?.msg || "Update failed");
    }
  };

  return (
    <div style={{ height: 600 }}>
      <Calendar
        localizer={localizer}
        events={events}
        defaultView="week"
        views={["week", "day", "agenda"]}
        step={30}
        showMultiDayTimes
        selectable
        resizable
        onEventDrop={onEventDrop}
        onEventResize={onEventDrop}
      />
    </div>
  );
}
