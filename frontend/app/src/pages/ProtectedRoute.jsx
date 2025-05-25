import { Navigate, useLocation } from "react-router-dom";
import { useContext } from "react";
import { UserContext } from "../contexts/UserContext";

const ProtectedRoute = ({ children }) => {
  const { user } = useContext(UserContext);
  const location = useLocation();

  if (!user) {
    // Сохраняем текущий путь для редиректа после авторизации
    return <Navigate to="/" state={{ from: location }} replace />;
  }

  return children;
};

export default ProtectedRoute;
