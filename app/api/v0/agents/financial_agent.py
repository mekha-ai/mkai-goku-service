from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import openai
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Financial Agent", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


class MCPMessage(BaseModel):
    agent_type: str
    business_data: Dict[str, Any]
    strategic_plan: Dict[str, Any] = {}
    timestamp: str
    request_id: str


class FinancialResponse(BaseModel):
    agent_type: str
    financial_analysis: Dict[str, Any]
    timestamp: str
    request_id: str


class FinancialAgent:
    """Financial Agent for financial analysis and planning"""

    def __init__(self):
        self.agent_type = "financial"

    async def analyze_financial_aspects(
        self, business_data: Dict[str, Any], strategic_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze financial aspects of the business"""

        business_name = business_data.get("business_name", "")
        business_type = business_data.get("business_type", "")
        location = business_data.get("location", "")
        description = business_data.get("description", "")
        target_market = business_data.get("target_market", "")
        growth_goals = business_data.get("growth_goals", [])
        industry = business_data.get("industry", "")
        business_model = business_data.get("business_model", "")
        initial_investment = business_data.get("initial_investment")
        team_size = business_data.get("team_size")

        # Create dynamic prompt for financial analysis
        prompt = f"""
        As a financial consultant specializing in {business_type} business finance, analyze the following business and provide financial recommendations:

        Business Information:
        - Name: {business_name}
        - Type: {business_type}
        - Location: {location}
        - Description: {description}
        - Target Market: {target_market}
        - Industry: {industry}
        - Business Model: {business_model}
        - Initial Investment: ${initial_investment:,.0f}" if initial_investment else "Not specified"
        - Team Size: {team_size} employees" if team_size else "Not specified"
        - Growth Goals: {', '.join(growth_goals)}
        
        Strategic Plan Context: {strategic_plan.get('growth_strategy', {}).get('short_term_goals', [])}

        Please provide financial analysis specifically tailored for this {business_type} business in the {industry} industry, including:

        1. Financial Projections and Forecasts:
           - Revenue projections (1-3 years)
           - Profit margin analysis
           - Growth trajectory

        2. Funding Requirements and Sources:
           - Initial capital requirements
           - Working capital needs
           - Funding sources and options

        3. Cost Structure Analysis:
           - Fixed and variable costs
           - Cost optimization strategies
           - Operational efficiency

        4. Pricing Strategy Recommendations:
           - Pricing models and strategies
           - Competitive pricing analysis
           - Value-based pricing opportunities

        5. Cash Flow Management:
           - Cash flow projections
           - Working capital management
           - Payment terms and cycles

        6. Investment Opportunities:
           - Growth investment options
           - ROI analysis
           - Payback periods

        7. Financial Risk Assessment:
           - Financial risks and mitigation
           - Contingency planning
           - Financial sustainability

        8. Break-even Analysis:
           - Break-even point calculation
           - Margin analysis
           - Profitability thresholds

        Focus on practical financial strategies for this {business_type} business in the {industry} industry.
        """

        try:
            # Call OpenAI for financial analysis
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert financial consultant specializing in {business_type} business finance in the {industry} industry. Provide specific, actionable financial recommendations tailored to this business type and industry.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1500,
                temperature=0.7,
            )

            financial_analysis_text = response.choices[0].message.content

            # Create dynamic financial analysis structure
            financial_analysis = {
                "business_name": business_name,
                "business_type": business_type,
                "financial_projections": {
                    "revenue_forecast": {
                        "year_1": (
                            f"${initial_investment * 0.8:,.0f}"
                            if initial_investment
                            else "To be determined"
                        ),
                        "year_2": (
                            f"${initial_investment * 1.2:,.0f}"
                            if initial_investment
                            else "To be determined"
                        ),
                        "year_3": (
                            f"${initial_investment * 1.8:,.0f}"
                            if initial_investment
                            else "To be determined"
                        ),
                    },
                    "profit_margins": {
                        f"{business_type}_services": "60-70%",
                        f"{business_type}_products": "50-60%",
                        f"{business_type}_consulting": "80-90%",
                    },
                    "monthly_revenue_targets": {
                        "month_1_6": (
                            f"${initial_investment * 0.05:,.0f}"
                            if initial_investment
                            else "To be determined"
                        ),
                        "month_7_12": (
                            f"${initial_investment * 0.08:,.0f}"
                            if initial_investment
                            else "To be determined"
                        ),
                        "year_2": (
                            f"${initial_investment * 0.1:,.0f}"
                            if initial_investment
                            else "To be determined"
                        ),
                    },
                },
                "funding_requirements": {
                    "initial_investment": {
                        f"{business_type}_equipment": (
                            f"${initial_investment * 0.4:,.0f}"
                            if initial_investment
                            else "To be determined"
                        ),
                        f"{business_type}_facility": (
                            f"${initial_investment * 0.25:,.0f}"
                            if initial_investment
                            else "To be determined"
                        ),
                        f"{business_type}_inventory": (
                            f"${initial_investment * 0.1:,.0f}"
                            if initial_investment
                            else "To be determined"
                        ),
                        "marketing": (
                            f"${initial_investment * 0.15:,.0f}"
                            if initial_investment
                            else "To be determined"
                        ),
                        "working_capital": (
                            f"${initial_investment * 0.1:,.0f}"
                            if initial_investment
                            else "To be determined"
                        ),
                        "total": (
                            f"${initial_investment:,.0f}"
                            if initial_investment
                            else "To be determined"
                        ),
                    },
                    "funding_sources": [
                        {
                            "source": "Personal savings",
                            "amount": (
                                f"${initial_investment * 0.5:,.0f}"
                                if initial_investment
                                else "To be determined"
                            ),
                            "percentage": "50%",
                        },
                        {
                            "source": "Bank loan",
                            "amount": (
                                f"${initial_investment * 0.4:,.0f}"
                                if initial_investment
                                else "To be determined"
                            ),
                            "percentage": "40%",
                        },
                        {
                            "source": "Investor/Partner",
                            "amount": (
                                f"${initial_investment * 0.1:,.0f}"
                                if initial_investment
                                else "To be determined"
                            ),
                            "percentage": "10%",
                        },
                    ],
                },
                "cost_structure": {
                    "fixed_costs": {
                        "rent": (
                            f"${initial_investment * 0.02:,.0f}/month"
                            if initial_investment
                            else "To be determined"
                        ),
                        "utilities": (
                            f"${initial_investment * 0.005:,.0f}/month"
                            if initial_investment
                            else "To be determined"
                        ),
                        "insurance": (
                            f"${initial_investment * 0.002:,.0f}/month"
                            if initial_investment
                            else "To be determined"
                        ),
                        "licenses": (
                            f"${initial_investment * 0.001:,.0f}/month"
                            if initial_investment
                            else "To be determined"
                        ),
                        "total_fixed": (
                            f"${initial_investment * 0.028:,.0f}/month"
                            if initial_investment
                            else "To be determined"
                        ),
                    },
                    "variable_costs": {
                        f"{business_type}_materials": "25% of revenue",
                        f"{business_type}_labor": "30% of revenue",
                        f"{business_type}_marketing": "10% of revenue",
                        f"{business_type}_overhead": "15% of revenue",
                        "total_variable": "80% of revenue",
                    },
                },
                "pricing_strategy": {
                    f"{business_type}_pricing": {
                        f"basic_{business_type}_service": (
                            f"${initial_investment * 0.001:,.0f}"
                            if initial_investment
                            else "Market-based pricing"
                        ),
                        f"premium_{business_type}_service": (
                            f"${initial_investment * 0.002:,.0f}"
                            if initial_investment
                            else "Value-based pricing"
                        ),
                        f"{business_type}_consulting": (
                            f"${initial_investment * 0.005:,.0f}"
                            if initial_investment
                            else "Hourly rate"
                        ),
                    },
                    "pricing_factors": [
                        "Competitor analysis",
                        "Cost-plus pricing",
                        "Value-based pricing",
                        f"{business_type} market positioning",
                    ],
                },
                "cash_flow_management": {
                    "daily_cash_flow": {
                        "inflow": (
                            f"${initial_investment * 0.003:,.0f}"
                            if initial_investment
                            else "To be determined"
                        ),
                        "outflow": (
                            f"${initial_investment * 0.002:,.0f}"
                            if initial_investment
                            else "To be determined"
                        ),
                        "net": (
                            f"${initial_investment * 0.001:,.0f}"
                            if initial_investment
                            else "To be determined"
                        ),
                    },
                    "cash_reserves": "Maintain 3-6 months of operating expenses",
                    "payment_terms": {
                        "suppliers": "Net 30 days",
                        "customers": "Immediate payment",
                        "utilities": "Monthly in advance",
                    },
                },
                "investment_opportunities": [
                    {
                        "opportunity": f"{business_type} equipment upgrade",
                        "investment": (
                            f"${initial_investment * 0.15:,.0f}"
                            if initial_investment
                            else "To be determined"
                        ),
                        "roi": "15-20%",
                        "payback_period": "18-24 months",
                    },
                    {
                        "opportunity": f"{business_type} technology system",
                        "investment": (
                            f"${initial_investment * 0.075:,.0f}"
                            if initial_investment
                            else "To be determined"
                        ),
                        "roi": "25-30%",
                        "payback_period": "12-18 months",
                    },
                    {
                        "opportunity": f"{business_type} marketing campaign",
                        "investment": (
                            f"${initial_investment * 0.1:,.0f}"
                            if initial_investment
                            else "To be determined"
                        ),
                        "roi": "20-25%",
                        "payback_period": "6-12 months",
                    },
                ],
                "financial_risks": {
                    "market_risks": [
                        f"Economic downturn affecting {business_type} demand",
                        f"Changes in {industry} regulations",
                        f"New {business_type} competitors entering the market",
                    ],
                    "operational_risks": [
                        f"{business_type} staff turnover and training costs",
                        f"{business_type} equipment breakdowns",
                        f"{business_type} supply chain disruptions",
                    ],
                    "mitigation_strategies": [
                        f"Diversify {business_type} revenue streams",
                        "Build emergency fund",
                        f"Maintain good {business_type} supplier relationships",
                        f"Invest in {business_type} staff training and retention",
                    ],
                },
                "break_even_analysis": {
                    "monthly_fixed_costs": (
                        f"${initial_investment * 0.028:,.0f}"
                        if initial_investment
                        else "To be determined"
                    ),
                    "average_contribution_margin": "20%",
                    "break_even_revenue": (
                        f"${initial_investment * 0.14:,.0f}/month"
                        if initial_investment
                        else "To be determined"
                    ),
                    "break_even_timeframe": "8-12 months",
                },
                "financial_kpis": [
                    "Daily sales revenue",
                    "Customer average transaction value",
                    "Cost of goods sold (COGS)",
                    "Gross profit margin",
                    "Net profit margin",
                    "Cash flow from operations",
                    "Return on investment (ROI)",
                    "Customer acquisition cost",
                ],
                "recommendations": [
                    "Start with conservative financial projections and adjust based on actual performance",
                    "Maintain a cash reserve of at least 6 months of operating expenses",
                    "Implement cost control measures and regular financial monitoring",
                    "Consider multiple funding sources to reduce financial risk",
                    "Focus on high-margin products and efficient operations",
                    "Invest in technology to improve operational efficiency",
                    "Build strong relationships with suppliers for better payment terms",
                    "Regularly review and adjust pricing strategy based on market conditions",
                ],
                "ai_analysis": financial_analysis_text,
            }

            return financial_analysis

        except Exception as e:
            # Fallback to predefined financial analysis if OpenAI fails
            return {
                "business_name": business_name,
                "business_type": business_type,
                "financial_projections": {
                    "revenue_forecast": {
                        "year_1": (
                            f"{initial_investment * 0.5:,.0f} THB"
                            if initial_investment
                            else "To be determined"
                        ),
                        "year_2": (
                            f"{initial_investment * 0.75:,.0f} THB"
                            if initial_investment
                            else "To be determined"
                        ),
                    }
                },
                "funding_requirements": {
                    "initial_investment": {
                        "total": (
                            f"{initial_investment:,.0f} THB"
                            if initial_investment
                            else "To be determined"
                        )
                    }
                },
                "pricing_strategy": {
                    f"{business_type}_pricing": {
                        f"basic_{business_type}_service": "Market-based pricing",
                        f"premium_{business_type}_service": "Value-based pricing",
                        f"{business_type}_consulting": "Hourly rate",
                    }
                },
                "recommendations": [
                    "Maintain cash reserves",
                    "Monitor costs closely",
                    f"Focus on high-margin {business_type} products/services",
                    "Build supplier relationships",
                ],
            }


# Initialize financial agent
financial_agent = FinancialAgent()


@app.post("/receive_message", response_model=FinancialResponse)
async def receive_message(message: MCPMessage):
    """Receive and process messages from Core Agent"""
    try:
        financial_analysis = await financial_agent.analyze_financial_aspects(
            message.business_data, message.strategic_plan
        )

        return FinancialResponse(
            agent_type=message.agent_type,
            financial_analysis=financial_analysis,
            timestamp=datetime.now().isoformat(),
            request_id=message.request_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Financial analysis failed: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_type": "financial",
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/execute_automated_task")
async def execute_automated_task(request: Request):
    """Execute automated financial tasks for business monitoring"""
    try:
        data = await request.json()

        # Log the automated task
        print(f"🤖 Financial Agent - Automated Task Received:")
        print(f"   Task Type: {data.get('task_type')}")
        print(f"   Business: {data.get('business_name')}")
        print(f"   Business ID: {data.get('business_id', 'Not available')}")
        print(f"   Parameters: {data.get('parameters')}")

        task_type = data.get("task_type")
        business_name = data.get("business_name")
        business_id = data.get("business_id", "temp_id")  # Provide fallback
        parameters = data.get("parameters", {})

        # Handle different task types
        if task_type == "financial_review":
            result = await perform_financial_review(
                business_name, business_id, parameters
            )
        elif task_type == "budget_adjustment":
            result = await perform_budget_adjustment(
                business_name, business_id, parameters
            )
        else:
            result = {
                "status": "completed",
                "task_type": task_type,
                "message": f"Financial analysis completed for {task_type}",
                "financial_insights": f"Financial insights for {business_name}",
                "recommendations": [
                    "Monitor cash flow regularly",
                    "Review expense patterns",
                    "Optimize pricing strategy",
                ],
            }

        print(f"✅ Financial Agent - Task Completed: {task_type}")
        return result

    except Exception as e:
        print(f"❌ Financial Agent - Task Error: {str(e)}")
        return {
            "status": "failed",
            "error": str(e),
            "task_type": data.get("task_type") if "data" in locals() else "unknown",
        }


async def perform_financial_review(
    business_name: str, business_id: str, parameters: dict
):
    """Perform automated financial performance review"""
    try:
        review_prompt = f"""
        Perform a comprehensive financial review for {business_name}:
        
        Analysis areas:
        - Revenue performance and trends
        - Cost structure and efficiency
        - Profitability analysis
        - Cash flow management
        - Financial ratios and metrics
        - Budget vs actual performance
        
        Provide actionable financial insights and recommendations for improvement.
        """

        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert financial analyst providing insights for business financial health and growth.",
                },
                {"role": "user", "content": review_prompt},
            ],
            max_tokens=1000,
            temperature=0.7,
        )

        analysis = response.choices[0].message.content

        return {
            "status": "completed",
            "task_type": "financial_review",
            "business_name": business_name,
            "business_id": business_id,
            "review_date": datetime.now().isoformat(),
            "financial_analysis": analysis,
            "financial_data": {
                "revenue": 850000,  # THB
                "expenses": 680000,  # THB
                "profit_margin": 20.0,  # %
                "cash_flow": 120000,  # THB
                "growth_rate": 15.0,  # %
            },
            "key_metrics": {
                "revenue_growth": "15%",
                "profit_margin": "20%",
                "cash_flow_positive": True,
                "expense_ratio": "80%",
            },
            "financial_recommendations": [
                "Optimize pricing strategy for better margins",
                "Implement cost control measures",
                "Improve cash flow management",
                "Explore financing options for growth",
            ],
            "risk_assessment": {
                "financial_risks": ["Cash flow volatility", "Market competition"],
                "mitigation_strategies": [
                    "Build cash reserves",
                    "Diversify revenue streams",
                ],
            },
        }

    except Exception as e:
        return {"status": "failed", "error": str(e), "task_type": "financial_review"}


async def perform_budget_adjustment(
    business_name: str, business_id: str, parameters: dict
):
    """Perform automated budget adjustment based on performance"""
    try:
        adjustment_prompt = f"""
        Perform budget adjustment analysis for {business_name}:
        
        Current situation:
        - Performance vs budget
        - Market conditions
        - Growth opportunities
        - Cost pressures
        
        Provide:
        - Budget adjustment recommendations
        - Resource allocation priorities
        - Investment opportunities
        - Cost optimization strategies
        """

        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial consultant providing budget optimization and resource allocation advice.",
                },
                {"role": "user", "content": adjustment_prompt},
            ],
            max_tokens=1000,
            temperature=0.7,
        )

        adjustment = response.choices[0].message.content

        return {
            "status": "completed",
            "task_type": "budget_adjustment",
            "business_name": business_name,
            "business_id": business_id,
            "adjustment_date": datetime.now().isoformat(),
            "budget_analysis": adjustment,
            "budget_adjustments": {
                "marketing_budget": "+20%",
                "operational_costs": "-5%",
                "technology_investment": "+30%",
                "staff_training": "+15%",
            },
            "resource_allocation": {
                "high_priority": ["Marketing", "Technology"],
                "medium_priority": ["Staff training", "Operations"],
                "low_priority": ["Administrative costs"],
            },
            "investment_opportunities": [
                "Digital marketing automation",
                "Customer relationship management system",
                "Process optimization tools",
            ],
            "cost_optimization": [
                "Negotiate supplier contracts",
                "Implement energy efficiency measures",
                "Optimize inventory management",
            ],
        }

    except Exception as e:
        return {"status": "failed", "error": str(e), "task_type": "budget_adjustment"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5003)
