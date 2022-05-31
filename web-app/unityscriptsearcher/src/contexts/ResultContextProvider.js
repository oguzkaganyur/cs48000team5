import React, { createContext, useContext, useState } from 'react';

const ResultContext = createContext();
const baseUrl = 'https://google-search3.p.rapidapi.com/api/v1';

export const ResultContextProvider = ({ children }) => {
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');

    const getResults = async (url) => {
        setLoading(true);

        const res = await fetch(`${baseUrl}${url}`, {
            method: 'GET',
            headers: {
                'X-User-Agent': 'desktop',
                'X-Proxy-Location': 'EU',
                'X-RapidAPI-Host': 'google-search3.p.rapidapi.com',
                'X-RapidAPI-Key': 'fb5c133520mshfbe823e2a2b412cp192492jsnb0188ada6573'
            },
        });

        const data = await res.json();

        setResults(data);
        setLoading(false);
    };

    return (
        <ResultContext.Provider value={{ getResults, results, searchTerm, setSearchTerm, loading }}>
            {children}
        </ResultContext.Provider>
    );
};

export const useResultContext = () => useContext(ResultContext);


/*
import React, {createContext, useContext, useState} from "react";

const ResultContext = createContext();
const baseUrl = 'https://google-search3.p.rapidapi.com/api/v1';

export const ResultContextProvider = ({children}) => {
    const [results, setResults] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');

    const getResults = async (type) => {
        setIsLoading(true);

        //videos search images
        const response = await fetch(`${baseUrl}${type}`,
            {
                method: 'GET',
                headers: {
                    'X-User-Agent': 'desktop',
                    'X-Proxy-Location': 'EU',
                    'X-RapidAPI-Host': 'google-search3.p.rapidapi.com',
                    'X-RapidAPI-Key': 'fb5c133520mshfbe823e2a2b412cp192492jsnb0188ada6573'
                }
            });

        const data = await response.json();

        console.log(data)

        setResults(data);
        setIsLoading(false);
    }

    return (
        <ResultContext.Provider value={{ getResults, results, searchTerm, setSearchTerm, isLoading }}>
            {children}
        </ResultContext.Provider>
    );

};

export const useResultContext = () => useContext(ResultContext);
 */