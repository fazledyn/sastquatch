const Navbar = () => {
  return (
    <nav className="bg-gray-800 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <span className="text-xl font-bold">Sastquatch Web</span>
            </div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <a href="/dashboard" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700">Dashboard</a>
                <a href="/logout" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700">Logout</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;