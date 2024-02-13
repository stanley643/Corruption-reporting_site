import React, { useState } from 'react';
import axios from 'axios';

function ReportForm() {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        axios.post('http://localhost:8000/api/reports/', { title, description })
            .then(res => console.log(res))
            .catch(err => console.error(err));
    };

    return (
        <form onSubmit={handleSubmit}>
            <input 
                type="text"
                value={title}
                onChange={e => setTitle(e.target.value)}
                placeholder="Title"
            />
            <textarea 
                value={description}
                onChange={e => setDescription(e.target.value)}
                placeholder="Description"
            />
            <button type="submit">Submit Report</button>
        </form>
    );
}

export default ReportForm;

