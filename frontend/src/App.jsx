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
      const response = await axios.get(`${API_BASE_URL}/tickets`);
      setTickets(response.data.tickets);
    } catch (err) {
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
