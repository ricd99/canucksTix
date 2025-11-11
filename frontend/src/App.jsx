import { useState, useEffect } from 'react';
import TicketList from './components/TicketList';
import { API_BASE_URL } from "./utils";
import axios from "axios";
import {BrowserRouter as Router, Routes, Route} from "react-router-dom"
import './App.css'

function App() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    fetchTickets();
  }, []);

  const fetchTickets = async () =>{
    setLoading(true);
    setError(null);

    try {
      console.log("🔄 Fetching tickets from:", `${API_BASE_URL}/tickets`);
      const response = await axios.get(`${API_BASE_URL}/tickets`);
      console.log("✅ Response received:", response.data);
      console.log("📊 Number of tickets:", response.data.length);
      setTickets(response.data);
    } catch (err) {
      if (err.response) {
        console.error("Response data:", err.response.data);
        console.error("Status:", err.response.status);
        console.error("Headers:", err.response.headers);
      } else if (err.request) {
        console.error("No response received:", err.request);
      } else {
        console.error("Error:", err.message);
      }
      setError("Failed to load tickets");   
    } finally {
      setLoading(false);
    }
    };

    if (loading) {
      return <div className="loading">Loading tickets...</div>;
    }

    if (error) {
      return <div className="error">{error}</div>;
    }

    return (
      <div className = "app">
        <header>
          <h1> Canucks tickets</h1>
          <p>Showing {tickets.length} tickets</p>
        </header>

        <TicketList tickets={tickets} />
      </div>
    );
  }

export default App
