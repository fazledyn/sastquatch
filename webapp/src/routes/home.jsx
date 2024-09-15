const HomePage = () => {
    return (
        <>
            <center>
                <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4 sm:px-6 lg:px-8">
                    <div className="max-w-md w-full space-y-8">
                        <h1 className="text-3xl">Sastquatch Web</h1>
                        <ul>
                            <li>
                                <a href="/login" className="text-xl hover:text-indigo-600">
                                    Log In to Continue
                                </a>
                            </li>
                            <li>
                                <a href="/register" className="text-xl hover:text-indigo-600">
                                    Register An Account
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </center>
        </>
    )
}

export default HomePage;
