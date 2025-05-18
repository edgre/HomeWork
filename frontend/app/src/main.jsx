import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "../src/assets/styles/index.css";
import App from "./App.jsx";
import AuthPage from "./pages/AuthPage.jsx";
import HomePage from "./pages/HomePage.jsx";
import CategoryPage from "./pages/CategoryPage.jsx";
import ProfilePage from "./pages/ProfilePage.jsx";
import NotFoundPage from "./pages/Notfoundpage.jsx";
import TaskPage from "./pages/TaskPage.jsx";
import TaskCreatePage from "./pages/TaskCreatePage.jsx";
import { UserProvider } from "./contexts/UserContext"; // Импортируем провайдер

const router = createBrowserRouter([
  {
    path: "/",
    element: <AuthPage />,
  },
  {
    path: "/home",
    element: <HomePage />,
  },
  {
    path: "/category/:slug",
    element: <CategoryPage />,
  },
  {
    path: "/category/:slug/:taskid",
    element: <TaskPage />,
  },
  {
    path: "/me",
    element: <ProfilePage />,
  },
  {
    path: "/create",
    element: <TaskCreatePage />,
  },
  {
    path: "*",
    element: <NotFoundPage />,
  },
]);

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <UserProvider> {/* Обертка для всего приложения */}
      <RouterProvider router={router} />
    </UserProvider>
  </StrictMode>
);