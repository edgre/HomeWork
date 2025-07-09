import React, { createContext, useState, useEffect, useCallback } from 'react';

/**
 * @typedef {Object} User
 * @property {number} id
 * @property {string} username
 * @property {string|null} realname
 * @property {number|null} rating
 * @property {boolean} has_drafts
 */

export const UserContext = createContext({
    user: null,
    isLoading: true,
    setUser: () => { },
    updateUser: () => { },
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
                localStorage.removeItem('access_token');
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

    const contextValue = {
        user,
        isLoading,
        error,
        setUser,
        updateUser,
    };

    return (
        <UserContext.Provider value={contextValue}>
            {children}
        </UserContext.Provider>
    );
};