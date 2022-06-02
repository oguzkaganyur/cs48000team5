import React, { createContext, useContext, useState } from 'react';
import axios from "axios";

const ResultContext = createContext();
const baseUrl = 'https://google-search3.p.rapidapi.com/api/v1';

export const ResultContextProvider = ({ children }) => {
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');

    const getResults = async (url) => {
        setLoading(true);

        console.log("searchTerm: ", searchTerm);


        const res = axios.post('http://localhost:5005/search', {
            query: searchTerm,
        })
            .then(function (response) {
                console.log("axios response: ", response);
                setResults(response.data);
                setLoading(false);

                console.log("res: ", res)
                console.log("response.data: ", response.data)
            })
            .catch(function (error) {
                console.log("axios error: ",error);
            });

        /*

                const res = await fetch(`${baseUrl}${url}`, {
                    method: 'GET',
                    headers: {
                        'X-User-Agent': 'desktop',
                        'X-Proxy-Location': 'EU',
                        'X-RapidAPI-Host': 'google-search3.p.rapidapi.com',
                        'X-RapidAPI-Key': 'fb5c133520mshfbe823e2a2b412cp192492jsnb0188ada6573'
                    },
                });
         */

        //const data = await res.json();

        //console.log("res: ", res)
        //console.log("data: ", data)

        //setResults(data);
        //setLoading(false);
    };

    return (
        <ResultContext.Provider value={{ getResults, results, searchTerm, setSearchTerm, loading }}>
            {children}
        </ResultContext.Provider>
    );
};

export const useResultContext = () => useContext(ResultContext);











/*
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
 */