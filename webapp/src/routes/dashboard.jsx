import axios from "axios";
import { useEffect, useState } from "react";
// local
import Navbar from '../components/navbar'

const Dashboard = () => {

    const [repos, setRepos] = useState([]);
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem("token")
        if (!isLoaded) {
            axios.get(
                `${import.meta.env.VITE_BACKEND_API_URL}/repositories`,
                {
                    headers: {
                        "Authorization": `Bearer ${token}`
                    }
                }
            ).then (
                res => res.data
            ).then (res => {
                if (res.success) {                
                    setRepos(res.data.repos)
                    setIsLoaded(true)
                }
                else {
                    alert(res.message)
                }
            })
        }
    })

    return (
        <>
            <Navbar />
            <div className="container mx-auto p-4">
                <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
                <div className="overflow-x-auto">
                    <table className="min-w-full bg-white">
                        <thead className="bg-gray-100">
                            <tr>
                                <th className="py-2 px-4 border-b text-left">Serial No.</th>
                                <th className="py-2 px-4 border-b text-left">Platform</th>
                                <th className="py-2 px-4 border-b text-left">Repository</th>
                                <th className="py-2 px-4 border-b text-left">Number of Bugs</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                repos.map((index, each) => {
                                    <tr key={index}>
                                        <td className="py-2 px-4 border-b">{index + 1}</td>
                                        <td className="py-2 px-4 border-b">{index.platform}</td>
                                        <td className="py-2 px-4 border-b">{index.owner}/{index.repo}</td>
                                        <td className="py-2 px-4 border-b">0</td>
                                    </tr>
                                })
                            }
                        </tbody>
                    </table>
                </div>
            </div>
        </>
    )
}

export default Dashboard;
