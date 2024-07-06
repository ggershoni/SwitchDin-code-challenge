import csv
import json
from datetime import datetime
from collections import defaultdict

# Global dictionaries to store our data
vpps = {}
sites = {}
batteries = {}
events = []


def create_vpp(name, revenue_percentage, daily_fee):
    vpps[name] = {
        'revenue_percentage': float(revenue_percentage),
        'daily_fee': float(daily_fee)
    }


def create_site(vpp_name, nmi, address):
    sites[nmi] = {
        'vpp_name': vpp_name,
        'address': address,
        'batteries': []
    }


def create_battery(nmi, manufacturer, serial_num, capacity):
    battery = {
        'manufacturer': manufacturer,
        'serial_num': serial_num,
        'capacity': float(capacity)
    }
    sites[nmi]['batteries'].append(battery)
    batteries[serial_num] = battery


def import_events(filename):
    global events
    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            events.append({
                'nmi': row['NMI'],
                'date': datetime.fromisoformat(row['DATE']),
                'energy': float(row['ENERGY']),
                'tariff': float(row['TARIFF'])
            })


def create_report(vpp_name, year_month):
    vpp = vpps[vpp_name]
    year, month = map(int, year_month.split('-'))

    # Filter events for the given month
    monthly_events = [e for e in events if e['date'].year == year and e['date'].month == month]

    # Calculate total revenue
    total_revenue = sum(e['energy'] * e['tariff'] for e in monthly_events)

    # Calculate VPP revenue
    vpp_revenue = total_revenue * (vpp['revenue_percentage'] / 100)

    # Calculate site revenues
    site_revenues = defaultdict(lambda: {'revenue': 0, 'daily_fees': 0})
    remaining_revenue = total_revenue - vpp_revenue

    # Calculate total capacity
    total_capacity = sum(sum(b['capacity'] for b in sites[nmi]['batteries']) for nmi in sites)

    for event in monthly_events:
        nmi = event['nmi']
        event_revenue = event['energy'] * event['tariff']
        site_revenues[nmi]['revenue'] += event_revenue * 0.8  # 80% to the site with the event

    # Distribute the remaining 20% based on capacity
    for nmi, site in sites.items():
        site_capacity = sum(b['capacity'] for b in site['batteries'])
        site_revenues[nmi]['revenue'] += remaining_revenue * 0.2 * (site_capacity / total_capacity)
        site_revenues[nmi]['daily_fees'] = vpp['daily_fee'] * 28  # Assuming 28 days per month
        vpp_revenue += site_revenues[nmi]['daily_fees']

    # Prepare the report
    report = {
        "vpp_name": vpp_name,
        "year_month": year_month,
        "total_revenue": total_revenue,
        "vpp_revenue": vpp_revenue,
        "site_revenues": [
            {
                "nmi": nmi,
                "revenue": data['revenue'],
                "daily_fees": data['daily_fees']
            } for nmi, data in site_revenues.items()
        ]
    }

    return json.dumps(report)