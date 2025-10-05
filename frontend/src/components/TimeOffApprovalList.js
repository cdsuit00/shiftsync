import { useEffect, useState } from "react";
import api from "../services/api";

export default function TimeOffApprovalList() {
  const [requests, setRequests] = useState([]);

  useEffect(() => {
    async function load() {
      try {
        const res = await api.get("/api/timeoff/");
        setRequests(res.data);
      } catch (err) {
        alert("Failed to load");
      }
    }
    load();
  }, []);

  const updateStatus = async (id, status) => {
    try {
      await api.put(`/api/timeoff/${id}/status`, { status });
      setRequests((r) => r.map((req) => (req.id === id ? { ...req, status } : req)));
    } catch (err) {
      alert("Action failed");
    }
  };

  return (
    <div>
      <h2>Time-off Approvals</h2>
      <table>
        <thead>
          <tr>
            <th>Employee</th>
            <th>Start</th>
            <th>End</th>
            <th>Reason</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {requests.map((r) => (
            <tr key={r.id}>
              <td>{r.user_name}</td>
              <td>{r.start_date}</td>
              <td>{r.end_date}</td>
              <td>{r.reason}</td>
              <td>{r.status}</td>
              <td>
                {r.status === "pending" && (
                  <>
                    <button onClick={() => updateStatus(r.id, "approved")}>Approve</button>
                    <button onClick={() => updateStatus(r.id, "denied")}>Deny</button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
