import { createContext, useState, useEffect, useCallback } from "react";
import api from "../services/api";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    try {
      const raw = localStorage.getItem("user");
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  });
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [loading, setLoading] = useState(false);

  // Auto-refresh token
  useEffect(() => {
    if (token) {
      localStorage.setItem("token", token);
      // Set up token refresh interval
      const refreshInterval = setInterval(() => {
        refreshToken();
      }, 55 * 60 * 1000); // Refresh 5 minutes before expiry
      
      return () => clearInterval(refreshInterval);
    } else {
      localStorage.removeItem("token");
    }
  }, [token]);

  useEffect(() => {
    if (user) {
      try {
        localStorage.setItem("user", JSON.stringify(user));
      } catch (e) {
        console.error("Failed to save user data");
      }
    } else {
      localStorage.removeItem("user");
    }
  }, [user]);

  const refreshToken = useCallback(async () => {
    try {
      const res = await api.post("/api/auth/refresh");
      setToken(res.data.access_token);
    } catch (err) {
      console.error("Token refresh failed:", err);
      logout();
    }
  }, []);

  const login = (tokenVal, userObj) => {
    setToken(tokenVal);
    setUser(userObj);
  };

  const logout = useCallback(() => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  }, []);

  const value = {
    user,
    token,
    login,
    logout,
    loading,
    setLoading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};