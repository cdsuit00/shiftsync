import { useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

export default function TimeOffRequestForm() {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [reason, setReason] = useState("");
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    try {
      await api.post("/api/timeoff/", { start_date: startDate, end_date: endDate, reason });
      alert("Submitted");
      navigate("/");
    } catch (err) {
      alert(err.response?.data?.msg || "Submission failed");
    }
  };

  return (
    <div className="form-card">
      <h2>Request Time Off</h2>
      <form onSubmit={submit}>
        <label>Start Date</label>
        <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} required />

        <label>End Date</label>
        <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} required />

        <label>Reason</label>
        <textarea value={reason} onChange={(e) => setReason(e.target.value)} />

        <button type="submit">Submit Request</button>
      </form>
    </div>
  );
}
