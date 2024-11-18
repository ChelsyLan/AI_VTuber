import { doc, getDoc } from "firebase/firestore";
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import Spinner from "../components/Spinner";
import { db } from "../firebase";
import { FaShare, FaLeaf, FaTint } from "react-icons/fa";
import { getAuth } from "firebase/auth";
import Contact from "../components/Contact";

export default function Listing() {
  const auth = getAuth();
  const params = useParams();
  const [listing, setListing] = useState(null);
  const [loading, setLoading] = useState(true);
  const [shareLinkCopied, setShareLinkCopied] = useState(false);
  const [contactSeller, setContactSeller] = useState(false);

  useEffect(() => {
    async function fetchListing() {
      const docRef = doc(db, "listings", params.listingId);
      const docSnap = await getDoc(docRef);
      if (docSnap.exists()) {
        setListing(docSnap.data());
        setLoading(false);
      }
    }
    fetchListing();
  }, [params.listingId]);

  if (loading) {
    return <Spinner />;
  }

  return (
    <main className="container mx-auto p-4">
      {/* Image Container */}
      <div className="relative w-full h-[400px] lg:h-[500px] mb-8 rounded-lg overflow-hidden shadow-md">
        <img
          src={listing.imgUrls[0]}
          alt={listing.name}
          className="w-full h-full object-cover"
        />
        <button
          onClick={() => {
            navigator.clipboard.writeText(window.location.href);
            setShareLinkCopied(true);
            setTimeout(() => setShareLinkCopied(false), 2000);
          }}
          className="absolute top-4 right-4 bg-white p-2 rounded-full shadow-lg hover:bg-gray-100 transition"
        >
          <FaShare className="text-xl text-gray-600" />
        </button>
        {shareLinkCopied && (
          <p className="absolute top-16 right-6 bg-white border border-gray-300 rounded-md p-2 shadow">
            Link Copied!
          </p>
        )}
      </div>

      {/* Listing Details */}
      <section className="bg-white p-6 rounded-lg shadow-lg space-y-4 lg:space-y-6">
        <h1 className="text-3xl font-bold text-gray-800">{listing.name}</h1>
        <h1 className="text-2xl font-semibold text-gray-800">
          Price:{" "}
          {listing.offer ? (
            <span>
              <span className="text-gray-500 line-through mr-2">
                ${listing.regularPrice.toLocaleString()}
              </span>
              <span className="text-green-700 font-bold">
                ${listing.discountedPrice.toLocaleString()}
              </span>
            </span>
          ) : (
            <span className="text-gray-800">
              ${listing.regularPrice.toLocaleString()}
            </span>
          )}
        </h1>

        {listing.offer && (
          <p className="text-sm font-semibold text-green-700 bg-green-100 p-2 rounded-md max-w-max shadow-sm">
            Save $
            {(
              +listing.regularPrice - +listing.discountedPrice
            ).toLocaleString()}
            !
          </p>
        )}

        <p className="flex items-center text-lg font-semibold text-gray-700">
          <FaLeaf className="text-green-600 mr-2" />
          Scent Profile: {listing.scent}
        </p>

        <p className="text-gray-700 text-lg leading-relaxed">
          <span className="font-semibold">Description:</span>{" "}
          {listing.description}
        </p>

        <ul className="flex flex-col sm:flex-row gap-4 text-md font-semibold text-gray-600">
          <li className="flex items-center">
            <FaTint className="text-blue-500 mr-2" />
            {+listing.size > 1 ? `${listing.size} ml` : "100 ml"}
          </li>
        </ul>

        {/* Contact Button */}
        {listing.userRef !== !contactSeller && (
          <button
            onClick={() => setContactSeller(true)}
            className="w-full py-3 mt-6 bg-blue-600 text-white font-medium rounded shadow-md hover:bg-blue-700 transition"
          >
            Contact Seller
          </button>
        )}
        {contactSeller && (
          <Contact userRef={listing.userRef} listing={listing} />
        )}
      </section>
    </main>
  );
}
