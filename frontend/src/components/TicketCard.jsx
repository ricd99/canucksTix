function TicketCard({ ticket }) {
  const ratingClasses = {
    EXCELLENT: "rating excellent",
    GOOD: "rating good",
    "FACE VALUE": "rating facevalue",
    INCOMPLETE: "rating incomplete",
    POOR: "rating poor",
  };

  const ratingClass =
    ratingClasses[ticket.rating?.toUpperCase()] || "rating incomplete";

  const price = ticket.price_per_ticket
    ? `$${ticket.price_per_ticket}`
    : "_____"; 
  const quantity = ticket.quantity || "missing";
  const location = ticket.location || null;
  const showMissingPrice = !ticket.price_per_ticket;

  return (
    <div className="ticket-card">
      <div className="ticket-header-grid">
        <span className={ratingClass}>
          {ticket.rating?.toUpperCase() || "INCOMPLETE"}
        </span>

        <span className="price">
          <span className={showMissingPrice ? "missing-price" : ""}>
            {price}
          </span>{" "}
          x {quantity}
        </span>

        {ticket.game && (
          <div className="ticket-game header-row">
            <strong>{ticket.game}</strong>
          </div>
        )}

        {location && (
          <div className="ticket-location header-row">
            <strong>{location}</strong>
          </div>
        )}
      </div>

      <div className="ticket-body">
        <p>{ticket.body || "missing"}</p>
      </div>

      <div className="ticket-footer">
        <span>By: {ticket.author || "unknown"}</span>
        <a href={ticket.permalink} target="_blank" rel="noopener noreferrer">
          View on Reddit
        </a>
      </div>
    </div>
  );
}

export default TicketCard;