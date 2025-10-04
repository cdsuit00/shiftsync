import { useState, useEffect } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

export default function ShiftForm() {
  const [users, setUsers] = useState([]);
  const [userId, setUserId] = useState("");
  const [title, setTitle] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [notes, setNotes] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    async function loadUsers() {
      try {
        const res = await api.get("/api/users/");
        setUsers(res.data);
        if (res.data.length) setUserId(res.data[0].id);
      } catch (err) {
        alert("Failed to load users");
      }
    }
    loadUsers();
  }, []);

  const submit = async (e) => {
    e.preventDefault();
    try {
      await api.post("/api/shifts/", {
        user_id: userId,
        title,
        start_time: new Date(startTime).toISOString(),
        end_time: new Date(endTime).toISOString(),
        notes,
      });
      alert("Shift created");
      navigate("/schedule");
    } catch (err) {
      alert(err.response?.data?.msg || "Error");
    }
  };

  return (
    <div className="form-card">
      <h2>Create Shift</h2>
      <form onSubmit={submit}>
        <label>Employee</label>
        <select value={userId} onChange={(e) => setUserId(e.target.value)}>
          {users.map((u) => (
            <option key={u.id} value={u.id}>
              {u.username}
            </option>
          ))}
        </select>

        <label>Title</label>
        <input value={title} onChange={(e) => setTitle(e.target.value)} required />

        <label>Start (local datetime)</label>
        <input type="datetime-local" value={startTime} onChange={(e) => setStartTime(e.target.value)} required />

        <label>End (local datetime)</label>
        <input type="datetime-local" value={endTime} onChange={(e) => setEndTime(e.target.value)} required />

        <label>Notes</label>
        <textarea value={notes} onChange={(e) => setNotes(e.target.value)} />

        <button type="submit">Create</button>
      </form>
    </div>
  );
}
