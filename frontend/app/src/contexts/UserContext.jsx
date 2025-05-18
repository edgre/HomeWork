// contexts/UserContext.js
import React, { createContext, useState, useEffect, useCallback } from 'react';

// Типы данных (для TypeScript)
/**
 * @typedef {Object} User
 * @property {string} username - Логин пользователя
 * @property {string|null} realname - Полное имя (может отсутствовать)
 * @property {number|null} rating - Рейтинг пользователя
 */

export const UserContext = createContext({
  user: null,
  setUser: () => {}
});

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Получение данных пользователя
  const fetchUserData = useCallback(async (token) => {
    try {
      const response = await fetch('/api/users/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Нормализация данных
      return {
        username: data.username,
        realname: data.realname,
        rating: parseFloat(data.rating),
      };
    } catch (err) {
      console.error('Ошибка загрузки данных:', err);
      setError(err.message);
      return null;
    }
  }, []);

  // Инициализация пользователя
  useEffect(() => {
    const initializeUser = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setIsLoading(false);
        return;
      }

      setIsLoading(true);
      const userData = await fetchUserData(token);
      setUser(userData);
      setIsLoading(false);
    };

    initializeUser();
  }, [fetchUserData]);

  return (
    <UserContext.Provider value={ [user,setUser]}>
      {children}
    </UserContext.Provider>
  );
};