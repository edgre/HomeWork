import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./assets/styles/index.css";
import { UserProvider } from "./contexts/UserContext";
import AuthPage from "./pages/AuthPage.jsx";
import HomePage from "./pages/HomePage.jsx";
import CategoryPage from "./pages/CategoryPage.jsx";
import ProfilePage from "./pages/ProfilePage.jsx";
import NotFoundPage from "./pages/NotFoundPage.jsx";
// import TaskPage from "./pages/TaskPage.jsx";
import TaskCreatePage from "./pages/TaskCreatePage.jsx";
import GdzPage from "./pages/GDZPage";
import ProtectedRoute from "./pages/ProtectedRoute"; // Импортируем новый компонент

const router = createBrowserRouter([
  {
    path: "/",
    element: <AuthPage />,
  },
  {
    path: "/home",
    element: <HomePage />, // Главная доступна без авторизации
  },
  {
    path: "/category/:slug",
    element: (
      <ProtectedRoute>
        <CategoryPage />
      </ProtectedRoute>
    ),
  },
  // {
  //     path: "/category/:slug/:taskid",
  //     element: (
  //         <ProtectedRoute>
  //             <TaskPage />
  //         </ProtectedRoute>
  //     ),
  // },
  {
    path: "/me",
    element: (
      <ProtectedRoute>
        <ProfilePage />
      </ProtectedRoute>
    ),
  },
  {
    path: "/gdz/:gdzId",
    element: (
      <ProtectedRoute>
        <GdzPage />
      </ProtectedRoute>
    ),
  },
  {
    path: "/create",
    element: (
      <ProtectedRoute>
        <TaskCreatePage />
      </ProtectedRoute>
    ),
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
