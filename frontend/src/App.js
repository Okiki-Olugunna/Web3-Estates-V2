import { useEffect, useState } from "react";
import { ethers } from "ethers";

// Components
import Navigation from "./components/Navigation";
import Search from "./components/Search";
import Home from "./components/Home";

// polygon mumbai contract addresses & abis
// real estate
import realEstateABI from "./utils/realEstateAbi.json";
const rABI = realEstateABI.realEstateABI;
const realEstateAddress = "0x842fBf41dF20193Aca9d4d6892D1812edd83F44D";
// escrow
import escrowABI from "./utils/escrowABI.json";
const eABI = escrowABI.escrowABI;
const escrowAddress = "0x7C782DD7eC9e362C04c61aeF110D751F22173C74";

function App() {
  // web3 provider
  const [provider, setProvider] = useState();
  // the current wallet connected
  const [account, setAccount] = useState();

  // the escrow contract
  const [escrow, setEscrow] = useState();

  // loading all the homes
  const [homes, setHomes] = useState([]);
  // loading a specific home when clicked on
  const [home, setHome] = useState({});
  // opens the specific home info
  const [toggle, setToggle] = useState(false);

  const loadBlockchainData = async () => {
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    // const provider = new ethers.providers.Web3Provider(ethereum, "any");
    setProvider(provider);
    // console.log(provider);

    const network = await provider.getNetwork();

    const realEstate = new ethers.Contract(realEstateAddress, rABI, provider);
    const totalSupply = await realEstate.totalSupply();
    console.log("The total supply of homes: ", totalSupply.toString());

    const homes = [];
    // getting all the homes/properties
    for (let i = 1; i <= totalSupply; i++) {
      const uri = await realEstate.tokenURI(i);
      const response = await fetch(uri);
      const metadata = await response.json();
      homes.push(metadata);
    }
    setHomes(homes);
    console.log("Homes: ", homes);

    const escrow = new ethers.Contract(escrowAddress, eABI, provider);
    setEscrow(escrow);

    window.ethereum.on("accountChanged", async () => {
      const accounts = await window.ethereum.request({
        method: "eth_requestAccounts",
      });
      const account = ethers.utils.getAddress(accounts[0]);
      const currentlyConnected = account.toUpperCase();
      setAccount(currentlyConnected);
    });

    console.log(`The currently connected account is: ${account}`);
  };

  // loading the blockchain data when the page reloads
  useEffect(() => {
    loadBlockchainData();
  }, []);

  // toggle to open up a specific house's info
  const togglePop = (home) => {
    // console.log(home);
    setHome(home);
    toggle ? setToggle(false) : setToggle(true);
  };

  return (
    <div>
      <Navigation account={account} setAccount={setAccount} />
      <Search />

      <div className="cards__section">
        <h3>Homes Available</h3>
        <hr></hr>

        <div className="cards">
          {homes.map((home, index) => (
            <div className="card" key={index} onClick={() => togglePop(home)}>
              <div className="card__image">
                <img src={home.image} alt="Home" />
              </div>
              <div className="card__info">
                <h4>{home.attributes[0].value} MATIC</h4>
                <p>
                  <strong>{home.attributes[2].value}</strong> bds |
                  <strong>{home.attributes[3].value}</strong> ba |
                  <strong>{home.attributes[4].value}</strong> sqft
                </p>
                <p>{home.address}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {toggle && (
        <Home
          home={home}
          provider={provider}
          account={account}
          escrow={escrow}
          togglePop={togglePop}
        />
      )}
    </div>
  );
}

export default App;
