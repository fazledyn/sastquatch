import { useState } from "react";
import { useParams } from "react-router-dom";
// local
import Navbar from '../components/navbar'


const Repository = () => {

    const {repositoryId} = useParams();

    const [repo, setRepo] = useState({});
    const [repoIsLoaded, setRepoIsLoaded] = useState(false);

    const [bugs, setBugs] = useState([]);
    const [bugsAreLoaded, setBugsAreLoaded] = useState(false);

    return (
        <>
            <Navbar />
            <div className="container mx-auto p-4">
                <h1 className="text-2xl font-bold mb-4">Repository</h1>
                <div className="overflow-x-auto">
                    <table className="min-w-full bg-white">
                        <thead className="bg-gray-100">
                            <tr>
                                <th className="py-2 px-4 border-b text-left">Serial No.</th>
                                <th className="py-2 px-4 border-b text-left">File Name</th>
                                <th className="py-2 px-4 border-b text-left">Bug Title</th>
                                <th className="py-2 px-4 border-b text-left">Line No.</th>
                                <th className="py-2 px-4 border-b text-left">External URL</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td className="py-2 px-4 border-b">"item.serialNo"</td>
                                <td className="py-2 px-4 border-b">"item.name"</td>
                                <td className="py-2 px-4 border-b">"item.number"</td>
                                <td className="py-2 px-4 border-b">"item.number"</td>
                                <td className="py-2 px-4 border-b">"item.number"</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </>
    )
}

export default Repository;
