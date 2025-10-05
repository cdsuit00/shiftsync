import { useEffect, useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

export default function ShiftList() {
  const [shifts, setShifts] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    async function loadShifts() {
      try {
        const res = await api.get("/api/shifts/");
        setShifts(res.data);
      } catch (err) {
        alert("Failed to load shifts");
      }
    }
    loadShifts();
  }, []);

  const deleteShift = async (id) => {
    if (!window.confirm("Are you sure?")) return;
    try {
      await api.delete(`/api/shifts/${id}`);
      setShifts(shifts.filter(s => s.id !== id));
    } catch (err) {
      alert("Delete failed");
    }
  };

  return (
    <div>
      <h2>Shifts</h2>
      <table>
        <thead>
          <tr>
            <th>Employee</th>
            <th>Title</th>
            <th>Start</th>
            <th>End</th>
            <th>Notes</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {shifts.map(s => (
            <tr key={s.id}>
              <td>{s.user_id}</td>
              <td>{s.title}</td>
              <td>{new Date(s.start_time).toLocaleString()}</td>
              <td>{new Date(s.end_time).toLocaleString()}</td>
              <td>{s.notes}</td>
              <td>
                <button onClick={() => deleteShift(s.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}