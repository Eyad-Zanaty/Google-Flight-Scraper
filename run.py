from pydoc import text
import random
import re
import time
from typing import Optional
from playwright.sync_api import sync_playwright, Playwright
from decouple import config
from fake_useragent import UserAgent
import pandas

def run(playwright: Playwright):
    useragent = UserAgent()
    userag = useragent.random
        
    browser = playwright.chromium.launch(
    headless=False,
    proxy={
                "server": config('proxy'),
                "username": config('username'),
                "password": config('password')
        }
    )

    context = browser.new_context(
        user_agent=userag
    )
    page= context.new_page()
    page.goto(config('site_url'))

    df= pandas.read_excel('source/destinations.xlsx')
    countries_list = df['city'].tolist()
    
    
    
    
    
    
    
    # Search the flight destination
    def flight_to(to_destination):
        to_airline = page.locator('input[aria-label*="Where to?"]').first
        to_airline.click(click_count=3)
        page.keyboard.type(to_destination)
        time.sleep(1)
        try:
            no_matching= page.locator('div[id="h0T7hb-9"] > div[role="alert"]').is_visible()
            no_matching.wait_for(state="visible", timeout=2000)
            print("No airport")
            return "No airport"
        except:
            pass
        to_list= page.locator('ul.DFGgtd[role="listbox"] > li[aria-label*="Airport"]').first
        to_list.click(force=True)
        
        return "Done"
    
    
    
    
    
    # Define a function to handle the nights selection
    def nights_selection(number_of_nights: int, counter: int):
            # time.sleep(3000)
            # Implement the logic for searching flights
            page.wait_for_load_state("networkidle")
            departure= page.locator('div.icWGef.A84apb.P0ukfb.bgJkKe div.BLohnc.q5Vmde').nth(0)
            departure.click()
            if counter >= 0:
                time.sleep(random.randint(2, 4))
                page.get_by_role("button", name="Reset").click()
            time.sleep(random.randint(1, 3))
            if number_of_nights < 7:
                less_nights= page.locator('div.ZGEB9c.yRXJAe.P0ukfb.icWGef.bgJkKe.BtDLie.iWO5td div.ZYDfBc.CQYfx > button.VfPpkd-LgbsSe').first
                reached_nights_number= page.locator('div.ZGEB9c.yRXJAe.P0ukfb.icWGef.bgJkKe.BtDLie.iWO5td div.ZYDfBc.CQYfx > span.Rx4ADb').inner_text().split(" ")[0]
                while int(reached_nights_number) > number_of_nights:
                    less_nights.click()
                    print("Clicked less nights button")
                    time.sleep(random.randint(1, 3))
                    reached_nights_number= page.locator('div.ZGEB9c.yRXJAe.P0ukfb.icWGef.bgJkKe.BtDLie.iWO5td div.ZYDfBc.CQYfx > span.Rx4ADb').inner_text().split(" ")[0]

            time.sleep(random.randint(1, 3))
            rows = page.locator('div[role="rowgroup"]')
            print("Total rows:", rows.count())
            
            price_list= []
            for i in range(1, rows.count()):
                d = rows.nth(i)
                try:
                    green_dates = d.locator('div.CylAxb.n3qw7.UNMzKf.julK3b.RZ6mCd').all()
                    for green_date in green_dates:
                        print(green_date.inner_text())
                        green_price= int(green_date.inner_text().replace("$", ""))
                        print(green_price)
                        price_list.append(green_price)

                except Exception as e:
                    print("No green")
                    continue
            
            next_button= page.locator('div.oB61Xb.E0vWmf.k8qXw div.d53ede.rQItBb.FfP4Bc.Gm3csc')
            
            for _ in range(10):
                try:
                    next_button.click()
                except Exception as e:
                    print("No next button")
                    break
                time.sleep(random.randint(1, 3))
                page.wait_for_timeout(1500) 

                rows = page.locator('div[role="rowgroup"]')
                print("Rows after next:", rows.count())

                for i in range(1, rows.count()):
                    d = rows.nth(i)
                    green_dates = d.locator('div.CylAxb.n3qw7.UNMzKf.julK3b.RZ6mCd').all()
                    for g in green_dates:
                        print("Price:", g.inner_text())
                        green_price= int(g.inner_text().replace("$", ""))
                        print(green_price)
                        price_list.append(green_price)
            
            least_price= min(price_list)
            print("Least Price:", least_price)
            


            price_found= False

            for i in range(1, rows.count()):
                d = rows.nth(i)
                try:
                    green_dates = d.locator('div.CylAxb.n3qw7.UNMzKf.julK3b.RZ6mCd').all()
                    for green_date in green_dates:
                        green_price= int(green_date.inner_text().replace("$", ""))
                        if green_price == least_price:
                            price_found= True
                            green_date.click()
                            print("Found and clicked least price:", green_price)
                            break
                        
                    if price_found:
                        break

                except Exception as e:
                    print("No green")
                    continue

            before_button= page.locator('div.oB61Xb.E0vWmf.k8qXw div.d53ede.QbVVHd.FfP4Bc.em0Hre.eLNT1d')
            
            if price_found== False:
                for _ in range(10):
                    try:
                        before_button.click()
                        print("Clicked before button")
                    except Exception as e:
                        print("No before button")
                        break
                    time.sleep(random.randint(1, 3))
                    page.wait_for_load_state("networkidle")
                    page.wait_for_timeout(1500) 

                    rows = page.locator('div[role="rowgroup"]')

                    for i in range(1, rows.count()):
                        d = rows.nth(i)
                        green_dates = d.locator('div.CylAxb.n3qw7.UNMzKf.julK3b.RZ6mCd').all()
                        for g in green_dates:
                            print("Price:", g.inner_text())
                            green_price= int(g.inner_text().replace("$", ""))
                            if green_price == least_price:
                                g.click()
                                price_found= True
                                print("Found and clicked least price:", green_price)
                                break
                        if price_found:
                            break
                    if price_found:
                        break
                
                time.sleep(random.randint(1, 3))
                
            for _ in range(number_of_nights+ 1):
                print("Pressing ArrowRight")
                page.keyboard.press("ArrowRight")
                page.wait_for_timeout(200) 
                
            time.sleep(random.randint(1, 3))
            # Pressing Done
            page.locator('div.akjk5c.FrVb0c > div.WXaAwc button[aria-label*="Done"]').first.click()
            
            return price_list

    
    def extract_flight_element_text(flight, selector: str, aria_label: Optional[str] = None) -> str:
        """Extract text from a flight element using selector and optional aria-label."""
        # time.sleep(300)  # Adding a delay to ensure the element is loaded
        if aria_label:
            element = flight.query_selector(f'{selector}[aria-label*="{aria_label}"]')
        else:
            element = flight.query_selector(selector)
        return element.inner_text() if element else "N/A"
    
    data=[]
    def scraping_flights(price_list):
        flights = page.query_selector_all('.pIav2d')
        for flight in flights:
            departure_time = extract_flight_element_text(flight, 'div', "Departure time:").split("â")[0]
            arrival_time =  extract_flight_element_text(flight, 'div', "Arrival time:").split("â")[0]
            from_airline = page.locator('input[aria-label*="Where from?"]').get_attribute('value')
            from_date= page.locator('div.GYgkab.YICvqf.kStSsc.ieVaIb').nth(0).get_attribute('data-value')
            stops= flight.query_selector("div.gQ6yfe.m7VU8c div div div div div div span.ogfYpf").inner_text()
            to_airline = page.locator('input[aria-label*="Where to?"]').get_attribute('aria-label').split("Where to? ")[1]
            to_date= page.locator('div.GYgkab.YICvqf.lJODHb.qXDC9e').nth(1).get_attribute('data-value')
            price =  extract_flight_element_text(flight, "div.FpEdX span")
            data.append({
                            "Departure Time": departure_time,
                            "Arrival Time": arrival_time,
                            "From": from_airline,
                            "From Date": from_date,
                            "Stops": stops,
                            "To": to_airline,
                            "To Date": to_date,
                            "Price": price,
                            "Green Prices": price_list
            })

            print(f"Departure Time: {departure_time}, Arrival Time: {arrival_time}, From: {from_airline}, From Date: {from_date}, To: {to_airline}, To Date: {to_date}, Price: {price}")



    # Running Flight Search

    # Selecting departure
    from_airline = page.locator('input[aria-label*="Where from?"]')
    from_airline.click(click_count=3)
    page.keyboard.type("Istanbul")
    time.sleep(1)
    from_list= page.locator('ul.DFGgtd[role="listbox"] > li[aria-label*="IST"]').click()
    
    # Selecting destination
    time.sleep(random.randint(1, 3))
    flight_to(countries_list[0])
    time.sleep(random.randint(1, 3))
    
    # Selecting date
    prices=nights_selection(3, -1)
    prices= list(dict.fromkeys(prices))
    time.sleep(random.randint(1, 3))

    # First search
    explore_button= page.locator('div.SS6Dqf.POQx1c[role="search"] div.xFFcie button').first
    explore_button.click()
    time.sleep(random.randint(1, 3))
    page.wait_for_load_state("networkidle")
    
    # Filters
    stops= page.locator('button[aria-label*="Stops"]').click()
    time.sleep(1)
    choose_stops= page.locator('div.PPUsDb > div[role="radiogroup"][aria-label*="Stops"] div.m76nmf').nth(2).click()
    time.sleep(random.randint(1, 3))
    try: 
        time.sleep(random.randint(1, 3))
        skip= page.locator('div.Bz9vRc.z0YF1 > div.WgNj4c  div[data-action="2"] button').first
        skip.wait_for(state="visible", timeout=500)
        skip.click()
    except Exception as e:
        print(f"Error selecting stops: {e}")
    page.wait_for_load_state("networkidle")
    # cheapest= page.locator('div.exIYg[id="M7sBEb"]').click()
    time.sleep(random.randint(1, 3))
    sortby= page.locator('button.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-Bz112c-UbuQg.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.ksBjEc.lKxP2d.LQeN7.zZJEBe').first.click()
    time.sleep(random.randint(1, 3))
    sortby_list= page.locator('ul.VfPpkd-StrnGf-rymPhb.DMZ54e > li[data-value="2"]').click()
    
    time.sleep(random.randint(1, 3))
    # Start scraping
    scraping_flights(prices)
    
    
    # Starting iterations
    counter= 0
    prices= []
    for country in countries_list[1:]:
        try:
            time.sleep(random.randint(2, 5))
            f= flight_to(country)
            if f == "No airport":
                continue
            time.sleep(random.randint(2, 5))
            page.wait_for_load_state("networkidle")
            prices= nights_selection(3, counter)
            prices= list(dict.fromkeys(prices))
            time.sleep(random.randint(2, 4))
            page.wait_for_load_state("networkidle")
            scraping_flights(prices)
            
            
            counter += 1
            if counter == 15:
                break
        except:
            print(f"Error occurred while processing {country}, skipping...")
            page.reload()
            page.wait_for_load_state("networkidle")
            continue
    

    df= pandas.DataFrame(data)
    df.to_csv("data/flight_data.csv", index=False)
    print("Data saved to CSV")

with sync_playwright() as playwright:
    run(playwright)