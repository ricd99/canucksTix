import TicketCard from './TicketCard';

function TicketList({ tickets }) {
    if (tickets.length === 0) {
        return <p className="no-tickets"> No tickets found</p>
    }

    return (
        <div className="ticket-list">
            {tickets.map(ticket => (
                <TicketCard key={ticket.id} ticket={ticket} />
            ))}
        </div>
    );
}

export default TicketList;