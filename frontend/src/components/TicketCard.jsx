function TicketCard({ ticket }) {
  const ratingClasses = {
    EXCELLENT: "rating excellent",
    GOOD: "rating good",
    FACE_VALUE: "rating facevalue",
    INCOMPLETE: "rating incomplete",
    POOR: "rating poor",
  };

  const ratingClass =
    ratingClasses[ticket.rating?.toUpperCase()] || "rating incomplete";

  const price = ticket.price_per_ticket
    ? `$${ticket.price_per_ticket}`
    : "_____"; 
  const quantity = ticket.quantity || "missing";
  const location = ticket.location || "missing";
  const showMissingPrice = !ticket.price_per_ticket;

  return (
    <div className="ticket-card">
      <div className="ticket-header">
        <span className={ratingClass}>
          {ticket.rating?.toUpperCase() || "INCOMPLETE"}
        </span>
        <span className="price">
          <span className={showMissingPrice ? "missing-price" : ""}>
            {price}
          </span>{" "}
          x {quantity}
        </span>
      </div>

      <div className="ticket-location">
        <strong>{location}</strong>
      </div>

      <div className="ticket-details">
        <p>
          <strong>Game:</strong> {ticket.game || "missing"}
        </p>
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
