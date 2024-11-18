import {
  collection,
  getDocs,
  limit,
  orderBy,
  query,
  where,
} from "firebase/firestore";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import ListingItem from "../components/ListingItem";
import { db } from "../firebase";
import { toast } from "react-toastify";

export default function Home() {
  const [offerListings, setOfferListings] = useState(null);
  const [liveData, setLiveData] = useState({
    live_link: null,
    name: null,
    chat_link: null,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchLiveData() {
      try {
        // Reference to the aiAgents collection
        const agentsRef = collection(db, "aiAgents");
        const q = query(agentsRef, where("campaignId", "==", "1"));
        const querySnap = await getDocs(q);

        if (!querySnap.empty) {
          const docData = querySnap.docs[0].data();
          setLiveData({
            live_link: docData.live_link,
            name: docData.name,
            chat_link: docData.chat_link,
          });
        } else {
          toast.error("Campaign not found");
        }
      } catch (error) {
        toast.error("Could not fetch live data");
      } finally {
        setLoading(false);
      }
    }

    fetchLiveData();
  }, []);

  const handleChatNow = () => {
    if (liveData.chat_link) {
      window.open(liveData.chat_link, "_blank");
    }
  };

  useEffect(() => {
    async function fetchListings() {
      try {
        const listingsRef = collection(db, "listings");
        const q = query(listingsRef, orderBy("timestamp", "desc"), limit(20));
        const querySnap = await getDocs(q);
        const listings = [];
        querySnap.forEach((doc) => {
          listings.push({
            id: doc.id,
            data: doc.data(),
          });
        });
        setOfferListings(listings);
      } catch (error) {
        console.log(error);
      }
    }
    fetchListings();
  }, []);

  return (
    <div className="max-w-6xl mx-auto pt-4 space-y-6">
      <div className="max-w-6xl mx-auto px-3">
        {loading ? (
          <p>Loading...</p>
        ) : liveData.live_link ? (
          <div className="flex flex-col items-center">
            <div className="relative w-full" style={{ paddingTop: "56.25%" }}>
              <iframe
                className="absolute top-0 left-0 w-full h-full"
                src={liveData.live_link}
                title={liveData.name || "YouTube Live Stream"}
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowFullScreen
              ></iframe>
            </div>
            <button
              onClick={handleChatNow}
              className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition duration-150"
            >
              Chat Now
            </button>
          </div>
        ) : (
          <p>SORRY OUR AI VTUBER IS CURRENTLY OFFLINE {liveData.name}</p>
        )}
      </div>
      <h2 className="px-3 text-2xl mt-6 font-semibold">
        Discover Our Perfumes
      </h2>
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
        {offerListings &&
          offerListings.map((listing) => (
            <Link to={`/listing/${listing.id}`} key={listing.id}>
              <ListingItem
                key={listing.id}
                listing={listing.data}
                id={listing.id}
              />
            </Link>
          ))}
      </div>
    </div>
  );
}
