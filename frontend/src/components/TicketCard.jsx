function TicketCard({ ticket }) {
    return (
        <div className="ticket-card">
            <div className="ticket-header">
                <span className={`rating ${ticket.rating}`}>{ticket.rating?.toUpperCase()}</span>
                <span className="price">${ticket.price_per_ticket} x {ticket.quantity}</span>
                <span className="location">${ticket.location}</span>
            </div>

            <div className="ticket-details">
                <p><strong>Game:</strong> {ticket.game}</p>
            </div>

            <div className="ticket-body">
                <p>{ticket.body}</p>
            </div>

            <div className="ticket-footer">
                <span>By: {ticket.author}</span>
                <a href={ticket.permalink} target="_blank" rel="noopener noreferrer">View on Reddit</a>
            </div>
        </div>
    );
}

export default TicketCard;