interface CardProps {
  title: string;
  body: string;
}

const Card = ({ title, body }: CardProps) => (
  <div className="card">
    <div className="card-body">
      <h3>{title}</h3>
      <p>{body}</p>
    </div>
  </div>
);

export default Card;
