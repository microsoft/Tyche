import React, { useEffect, useState } from "react";

function Tickets() {
  const [tickets, setTickets] = useState([]);

  // ...existing code...
useEffect(() => {
  fetch("https://zany-space-bassoon-jvxgqxrg5q9h45g-8000.app.github.dev/api/tickets")
    .then((res) => res.json())
    .then((data) => setTickets(data))
    .catch((err) => console.error("Error fetching tickets:", err));
}, []);
// ...existing code...

  return (
    <div>
      <h2>Tickets</h2>
      <ul>
        {tickets.map((ticket, idx) => (
          <li key={idx}>
            {ticket.ticket_number} - {ticket.subject}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Tickets;