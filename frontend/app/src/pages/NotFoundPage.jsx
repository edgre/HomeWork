import { Link } from "react-router-dom";

const NotFoundPage = () => {
  return (
    <div>
      <h1> {"Not Found Page :("}</h1>
      <Link to={"/"}>
        <button className="button">Home</button>
      </Link>
    </div>
  );
};

export default NotFoundPage;
