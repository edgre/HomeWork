import { Navigate, useLocation } from "react-router-dom";
import { useContext, useEffect, useState } from "react";
import { UserContext } from "../contexts/UserContext";

const ProtectedRoute = ({ children }) => {
    const { user, isLoading } = useContext(UserContext);
    const location = useLocation();
    const [isChecking, setIsChecking] = useState(true);

    useEffect(() => {
        if (!isLoading) {
            setIsChecking(false);
        }
    }, [isLoading]);

    if (isChecking) {
        return null;
    }

    if (!user) {
        return <Navigate to="/" state={{ from: location }} replace />;
    }

    return children;
};

export default ProtectedRoute;