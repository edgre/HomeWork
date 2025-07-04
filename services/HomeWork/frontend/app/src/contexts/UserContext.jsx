import React, { createContext, useState, useEffect, useCallback } from 'react';


export const UserContext = createContext({
  user: null,
  setUser: () => {
    console.warn('setUser called without Provider');
  }
});

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

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

      return {
        id: data.id,
        username: data.username,
        realname: data.realname,
        rating: data.rating ? parseFloat(data.rating) : null,
        has_drafts: data.has_drafts
      };
    } catch (err) {
      console.error('Ошибка загрузки данных:', err);
      setError(err.message);
      return null;
    }
  }, []);

  useEffect(() => {
    const initializeUser = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setIsLoading(false);
        return;
      }

      setIsLoading(true);
      try {
        const userData = await fetchUserData(token);
        setUser(userData);
      } catch (err) {
        console.error('Ошибка инициализации:', err);
      } finally {
        setIsLoading(false);
      }
    };

    initializeUser();
  }, [fetchUserData]);

    const updateUser = (updates) => {
    setUser((prevUser) => ({
      ...prevUser,
      ...updates,
    }));
  };

  return (
    <UserContext.Provider value={{ user, setUser, updateUser }}>
      {children}
    </UserContext.Provider>
  );
};