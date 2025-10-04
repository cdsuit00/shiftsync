import { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import { Link } from "react-router-dom";
import api from "../services/api";

export default function Dashboard() {
  const { user, logout } = useContext(AuthContext);
  const [counts, setCounts] = useState({ shifts: 0, timeoff: 0 });

  useEffect(() => {
    async function load() {
      try {
        const shifts = await api.get("/api/shifts");
        const timeoff = await api.get("/api/timeoff");
        setCounts({ shifts: shifts.data.length, timeoff: timeoff.data.length });
      } catch (err) {
        // ignore - user might be unauthorized
      }
    }
    load();
  }, []);

  return (
    <div className="dashboard">
      <header>
        <h1>Welcome, {user.username}</h1>
        <div>Role: {user.role}</div>
        <button onClick={logout}>Logout</button>
      </header>

      <section className="cards">
        <div className="card">
          <h3>Shifts</h3>
          <p>{counts.shifts}</p>
          <Link to="/schedule">View schedule</Link>
          {user.role === "manager" && <Link to="/shift/new">Create shift</Link>}
        </div>

        <div className="card">
          <h3>Time-off</h3>
          <p>{counts.timeoff}</p>
          <Link to="/timeoff/new">Request time off</Link>
          {user.role === "manager" && <Link to="/approvals">Approvals</Link>}
        </div>
      </section>
    </div>
  );
}
