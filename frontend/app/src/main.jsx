import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./assets/styles/index.css";
import { UserProvider } from "./contexts/UserContext";
import AuthPage from "./pages/AuthPage.jsx";
import HomePage from "./pages/HomePage.jsx";
import CategoryPage from "./pages/CategoryPage.jsx";
import ProfilePage from "./pages/ProfilePage.jsx";
import NotFoundPage from "./pages/Notfoundpage.jsx";
import TaskPage from "./pages/TaskPage.jsx";
import TaskCreatePage from "./pages/TaskCreatePage.jsx";
import GdzPage from "./pages/GdzPage";

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
     path: "/gdz/:gdzId",
     element: <GdzPage />,
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
    <UserProvider>
      <RouterProvider router={router} />
    </UserProvider>
  </StrictMode>
);