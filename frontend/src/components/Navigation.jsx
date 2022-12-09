import logo from "../assets/logo.svg";
import { ethers, utils  } from "ethers";

const Navigation = ({ account, setAccount }) => {
  const connectHandler = async () => {
    // getting the chainid of the current network the user is connected to
    const chainId = await window.ethereum.request({ method: "eth_chainId" });
    console.log("The current chain ID is:", chainId)

    const mumbai = utils.hexValue(80001);
    if (chainId !== mumbai) {
      // switching the user's network to Mumbai
      console.log("Switching network to Mumbai...")

      await window.ethereum.request({
        method: "wallet_switchEthereumChain",
        params: [{ chainId: mumbai }],
      });

      console.log("Success.")
    }

    // connecting account
    console.log("Connecting account...")

    const accounts = await window.ethereum.request({
      method: "eth_requestAccounts",
    });
    const currentlyConnected = await accounts[0];
    setAccount(currentlyConnected.toUpperCase());

    console.log("Success.")
    console.log(`The currently connected account is: ${account}`, account);
  };

  return (
    <nav>
      <ul className="nav__links">
        <li>
          <a href="#">Buy</a>
        </li>
        <li>
          <a href="#">Rent</a>
        </li>
        <li>
          <a href="#">Sell</a>
        </li>
      </ul>

      <div className="nav__brand">
        <img src={logo} alt="Logo" />
        <h1>WEB3 ESTATES</h1>
      </div>

      {account ? (
        <button type="button" className="nav__connect">
          {account.slice(0, 6) + "..." + account.slice(38, 42)}
        </button>
      ) : (
        <button type="button" className="nav__connect" onClick={connectHandler}>
          Connect Wallet
        </button>
      )}
    </nav>
  );
};

export default Navigation;
