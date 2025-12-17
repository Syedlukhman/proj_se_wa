/*
 * book_listings.js
 *
 * This file defines a small React application that renders the recent
 * book listings on the home page and provides a dynamic search
 * experience. Users can type into the search bar and the listing
 * grid updates in real time. The component expects a global
 * `listingsData` variable defined in the HTML template which
 * contains an array of listing objects with `id`, `title`,
 * `author`, `genre`, and `condition` properties.
 */

// Ensure React and ReactDOM are loaded from the CDN. We guard
// against accidental multiple mounts by checking for the
// presence of the root element on DOMContentLoaded.
document.addEventListener('DOMContentLoaded', () => {
    const rootEl = document.getElementById('listing-root');
    if (!rootEl || typeof React === 'undefined' || typeof ReactDOM === 'undefined') {
        // If React or the root element isn't available, do nothing.
        return;
    }
    // Define a simple card component for each listing
    function ListingCard({ listing }) {
        return (
            React.createElement('div', { className: 'bg-white rounded-lg shadow p-4 flex flex-col justify-between' },
                [
                    React.createElement('div', { key: 'content' }, [
                        React.createElement('h3', { key: 'title', className: 'text-xl font-semibold mb-2' }, listing.title),
                        React.createElement('p', { key: 'author', className: 'mb-1' },
                            React.createElement('span', { className: 'font-medium' }, 'Author: '), listing.author
                        ),
                        listing.genre ? React.createElement('p', { key: 'genre', className: 'mb-1' },
                            React.createElement('span', { className: 'font-medium' }, 'Genre: '), listing.genre
                        ) : null,
                        React.createElement('p', { key: 'condition', className: 'mb-2' },
                            React.createElement('span', { className: 'font-medium' }, 'Condition: '), listing.condition || 'Unknown'
                        )
                    ]),
                    React.createElement('a', { key: 'link', href: `/listing/${listing.id}`, className: 'mt-auto inline-block bg-blue-600 hover:bg-blue-700 text-white py-2 px-3 rounded text-center' }, 'View Details')
                ]
            )
        );
    }

    // Main App component
    function ListingsApp() {
        const [searchTerm, setSearchTerm] = React.useState('');

        // Filter listings based on the search term (case‑insensitive)
        const filteredListings = React.useMemo(() => {
            if (!Array.isArray(listingsData)) return [];
            return listingsData.filter(item => {
                const term = searchTerm.toLowerCase();
                return (
                    item.title.toLowerCase().includes(term) ||
                    item.author.toLowerCase().includes(term) ||
                    (item.genre && item.genre.toLowerCase().includes(term)) ||
                    (item.condition && item.condition.toLowerCase().includes(term))
                );
            });
        }, [searchTerm]);

        return (
            React.createElement('div', { className: 'space-y-6' }, [
                React.createElement('div', { key: 'search', className: 'flex flex-col sm:flex-row items-center gap-2' }, [
                    React.createElement('input', {
                        key: 'input',
                        type: 'text',
                        placeholder: 'Search listings…',
                        value: searchTerm,
                        onChange: (e) => setSearchTerm(e.target.value),
                        className: 'w-full sm:flex-1 p-2 border border-gray-300 rounded'
                    }),
                    React.createElement('p', { key: 'count', className: 'text-sm text-gray-600' }, `${filteredListings.length} result${filteredListings.length !== 1 ? 's' : ''}`)
                ]),
                React.createElement('div', { key: 'grid', className: 'grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4' },
                    filteredListings.map(listing => React.createElement(ListingCard, { key: listing.id, listing }))
                ),
                React.createElement('div', { key: 'browseLink', className: 'text-center' },
                    React.createElement('a', { href: '/listings', className: 'text-blue-600 hover:underline' }, 'Browse all listings »')
                )
            ])
        );
    }

    // Mount the React app
    ReactDOM.createRoot(rootEl).render(React.createElement(ListingsApp));
});