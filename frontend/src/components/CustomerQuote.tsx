interface CustomerQuoteProps {
  quote: string;
  name: string;
  description: string;
  avatar: string;
}

const CustomerQuote = ({ quote, name, description, avatar }: CustomerQuoteProps) => (
  <div className="customer-quote">
    <p>{quote}</p>
    <div className="quote-info">
      <img className="avatar" alt="Avatar" src={avatar} />
      <div>
        <div>{name}</div>
        <div>{description}</div>
      </div>
    </div>
  </div>
);

export default CustomerQuote;
