import { customerQuotes, cards } from "../data/landingPage";
import CustomerQuote from "../components/CustomerQuote";
import Card from "../components/Card";
import HeroSection from "../components/HeroSection";
import Navigation from "../components/Navigation";
import FooterNav from "../components/FooterNav";
import CreateAccountForm from "../components/CreateAccountForm";

export const LandingPage = () => {
  return (
    <div className="landing-page">
      <Navigation />

      <HeroSection />

      <section className="quotes-section">
        {customerQuotes.map((q, i) => (
          <CustomerQuote key={i} {...q} />
        ))}
      </section>

      <section className="cards-section">
        {cards.map((c, i) => (
          <Card key={i} {...c} />
        ))}
      </section>

      <CreateAccountForm />

      <FooterNav />
    </div>
  );
};
