import { useContext } from "react";
import { Routes, Route, Link, Navigate } from "react-router-dom";
import LoginForm from "./components/LoginForm";
import SignupForm from "./components/SignupForm";
import Dashboard from "./components/Dashboard";
import ScheduleCalendar from "./components/ScheduleCalendar";
import ShiftForm from "./components/ShiftForm";
import ShiftList from "./components/ShiftList";
import TimeOffRequestForm from "./components/TimeOffRequestForm";
import TimeOffApprovalList from "./components/TimeOffApprovalList";
import { AuthContext } from "./context/AuthContext";

const PrivateRoute = ({ children, roles }) => {
  const { user } = useContext(AuthContext);
  if (!user) return <Navigate to="/login" replace />;
  if (roles && !roles.includes(user.role)) return <Navigate to="/" replace />;
  return children;
};

export default function App() {
  return (
    <div className="app">
      <nav className="navbar">
        <Link to="/">ShiftSync</Link>
        <div>
          <Link to="/">Dashboard</Link> | <Link to="/schedule">Schedule</Link>
        </div>
      </nav>

      <Routes>
        <Route path="/login" element={<LoginForm />} />
        <Route path="/signup" element={<SignupForm />} />
        <Route
          path="/"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />
        <Route
          path="/schedule"
          element={
            <PrivateRoute>
              <ScheduleCalendar />
            </PrivateRoute>
          }
        />
        <Route
          path="/shift/new"
          element={
            <PrivateRoute roles={["manager"]}>
              <ShiftForm />
            </PrivateRoute>
          }
        />
        <Route
          path="/timeoff/new"
          element={
            <PrivateRoute roles={["employee", "manager"]}>
              <TimeOffRequestForm />
            </PrivateRoute>
          }
        />
        <Route
          path="/approvals"
          element={
            <PrivateRoute roles={["manager"]}>
              <TimeOffApprovalList />
            </PrivateRoute>
          }
        />
        <Route
          path="/shifts"
          element={
            <PrivateRoute roles={["manager"]}>
              <ShiftList />
            </PrivateRoute>
          }
        />
      </Routes>
    </div>
  );
}
