---
layout: post
title: Visualizing personal finances
author: Aaron Stacy
---

## TL;DR

[Click here to see the visualizations with some example data](/personal-finances-dashboard).

## Background

In order to get on the same page about money, my wife and I sit down each month and review where we're at financially. This dashboard helps discuss questions like:

- Where did all of our spending go last month?
- How does last month's spending compare with previous months?
- How far along are we in our yearly savings goals?
- How much of our income are we saving?
- How much have we earned from our investments?
- What's our net worth?
- How much of our income are we giving to worthy causes/non-profits?
- How does our giving, saving, and tax rate change as our income changes?

## How does it work?

We track all of our transactions in [a program like QuickBooks, but for programmer nerds](https://beancount.github.io). Then I run some Python scripts to generate the report that contains last month's data as well as our historical financial information. Since all of the information is derived from a ledger of transactions, it's straightforward to go back and generate old reports, but I keep a directory of the files to access them easily.

The data is [a big pile of JSON](/personal-finances-dashboard/data.js), and the report itself is just an HTML file. I use [D3.js](https://d3js.org) for the visualizations.

## Why this approach?

This is more work than most people need, but I took this approach for a number of reasons:

1. Apps like Mint are nice for tracking expenses, but since it's not a [double-entry ledger](https://en.wikipedia.org/wiki/Double-entry_bookkeeping), it's not good at modeling money moving between accounts, money you're owed, etc.

1. Apps like Personal Capital are nice for tracking assets in big investment firms, but there are a lot of systems they don't integrate well with, so the data is never quite accurate.

1. I couldn't find a good way of tracking cost basis and investment growth across financial services providers.

1. Between payroll, retirement, brokerage, HSA, etc., logging into all of these separate portals it gets time consuming when you need to check information. Once it's imported into an accounting ledger, you can just look at that.

1. Spreadsheets are great for tracking things like giving/saving/taxes over the years. Most people should probably use these, and this worked really well for me at first.

    But in my case, once I got all of my information into a ledger, the copy/pasting became error prone and tedious. It's nice that once I do the work of booking and reconciling transactions, I can easily get a complete picture of the state of our finances.

1. Tools like Jupyter and Colab are powerful, and I think they're a great fit for programmatic accounting like [Ledger CLI](https://www.ledger-cli.org) and [Beancount](https://beancount.github.io/docs/index.html). These notebooks also worked for me for a time, and it'd be really cool to see more examples of personal finances notebooks, but I found the charting capabilities really lacking.

    [Bokeh](https://docs.bokeh.org/en/latest/) was the best option I found, but there were a lot of details I found frustrating that I couldn't easily fix (i.e. getting more context and precision in tooltips).

    I was already writing code to generate the data and format that into something the charting library could use, and since I've got a background in web development, it wasn't a big leap to translate the notebooks into scripts that generated HTML files.

## Future work

Listen we're all busy, and this is a side project. But a few things that'd be nice to fix up:

- Accessibility
- Responsiveness / mobile friendliness
- Cross-browser animations &emdash; I learned that Blink animates the `d` attribute of SVG elements, but WebKit does not. I couldn't even find a [caniuse.com](https://caniuse.com) link, but [CSS tricks references this](https://css-tricks.com/svg-properties-and-css/#aa-wrapping-up). So you'll notice the the only animation in Safari is switching the networth chart between total gains and value+cost basis. It's so clean to use CSS for the rest of the animations, I'm not inclined to migrate those to JS.
- More data and charts:
  - My dad tells me I should add a button to adjust everything for inflation. I see where he's going with this, and maybe it's a good exercise in empathy.
  - Provide a breakdown of the cost basis/value chart on a per-asset basis.
  - Top + bottom 3 assets for internal rates of return (spoiler alert: BTC is at the bottom).
- Post the scripts that generate the data. This is tricky because:
  1. There are a lot of assumptions baked into them (it'd be hard to visualize all of this across different currencies).
  1. There is a lot of personal information that is hard to generalize (i.e. account names).
- Hosting &emdash; hosting static HTML pages can be pretty secure, so it'd be nice to i.e. hook this up to a GitHub workflow that posted them on a private pages site.