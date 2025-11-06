"""
Business logic services cho Finance.
"""
from typing import Dict, List
from datetime import datetime, date
from django.db.models import Sum, Count, Q, F
from apps.projects.models import Project
from apps.salaries.models import Salary, MonthlySalary
from apps.partners.models import Partner


class FinanceService:
    """Service class cho xử lý logic tài chính."""

    @staticmethod
    def monthly_overview(month: str) -> Dict:
        """
        Tổng quan tài chính tháng.

        Args:
            month: Tháng (YYYY-MM)

        Returns:
            Dict chứa tổng quan tài chính
        """
        # Parse month
        year, month_num = map(int, month.split('-'))

        # Get projects in month
        projects = Project.objects.filter(
            shoot_date__year=year,
            shoot_date__month=month_num
        )

        # Calculate revenue
        total_revenue = 0
        completed_revenue = 0
        pending_revenue = 0

        for project in projects:
            revenue = float(project.package_final_price)
            total_revenue += revenue

            if project.status == 'completed':
                completed_revenue += revenue
            else:
                pending_revenue += revenue

        # Calculate costs
        # 1. Salary costs
        salary_costs = MonthlySalary.objects.filter(month=month).aggregate(
            total=Sum('total_salary')
        )['total'] or 0

        # 2. Partner costs
        partner_costs = 0
        for project in projects:
            if project.partners and 'total_cost' in project.partners:
                partner_costs += float(project.partners.get('total_cost', 0))

        total_costs = float(salary_costs) + partner_costs

        # Calculate profit
        total_profit = total_revenue - total_costs

        # Revenue breakdown
        revenue_breakdown = {
            'completed': completed_revenue,
            'pending': pending_revenue,
            'total': total_revenue
        }

        # Cost breakdown
        cost_breakdown = {
            'salaries': float(salary_costs),
            'partners': partner_costs,
            'total': total_costs
        }

        return {
            'month': month,
            'total_revenue': total_revenue,
            'total_costs': total_costs,
            'total_profit': total_profit,
            'revenue_breakdown': revenue_breakdown,
            'cost_breakdown': cost_breakdown,
            'project_count': projects.count(),
            'completed_project_count': projects.filter(status='completed').count()
        }

    @staticmethod
    def calculate_profit(
        from_date: date,
        to_date: date
    ) -> Dict:
        """
        Tính lợi nhuận trong khoảng thời gian.

        Args:
            from_date: Từ ngày
            to_date: Đến ngày

        Returns:
            Dict chứa thông tin lợi nhuận
        """
        # Get projects in period
        projects = Project.objects.filter(
            shoot_date__gte=from_date,
            shoot_date__lte=to_date
        )

        total_revenue = 0
        total_costs = 0
        project_details = []

        for project in projects:
            revenue = float(project.package_final_price)

            # Calculate project costs
            salary_cost = 0
            if project.team:
                # Main photographer
                if project.team.get('main_photographer'):
                    salary_cost += float(project.team['main_photographer'].get('salary', 0))
                    salary_cost += float(project.team['main_photographer'].get('bonus', 0))

                # Assist photographers
                for member in project.team.get('assist_photographers', []):
                    salary_cost += float(member.get('salary', 0))
                    salary_cost += float(member.get('bonus', 0))

                # Makeup artists
                for member in project.team.get('makeup_artists', []):
                    salary_cost += float(member.get('salary', 0))
                    salary_cost += float(member.get('bonus', 0))

                # Retouch artists
                for member in project.team.get('retouch_artists', []):
                    salary_cost += float(member.get('salary', 0))
                    salary_cost += float(member.get('bonus', 0))

            partner_cost = 0
            if project.partners:
                partner_cost = float(project.partners.get('total_cost', 0))

            project_total_cost = salary_cost + partner_cost
            project_profit = revenue - project_total_cost

            total_revenue += revenue
            total_costs += project_total_cost

            project_details.append({
                'project_id': str(project.id),
                'project_code': project.project_code,
                'customer_name': project.customer_name,
                'revenue': revenue,
                'costs': project_total_cost,
                'profit': project_profit,
                'profit_margin': (project_profit / revenue * 100) if revenue > 0 else 0
            })

        profit = total_revenue - total_costs
        profit_margin = (profit / total_revenue * 100) if total_revenue > 0 else 0

        return {
            'period': f"{from_date} to {to_date}",
            'total_revenue': total_revenue,
            'total_costs': total_costs,
            'profit': profit,
            'profit_margin': profit_margin,
            'projects': project_details
        }

    @staticmethod
    def project_finance_detail(project_id: str) -> Dict:
        """
        Chi tiết tài chính của dự án.

        Args:
            project_id: ID dự án

        Returns:
            Dict chứa chi tiết tài chính
        """
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return None

        revenue = float(project.package_final_price)

        # Calculate costs
        costs = {
            'salaries': 0,
            'partners': 0,
            'other': 0
        }

        # Salary costs
        if project.team:
            if project.team.get('main_photographer'):
                costs['salaries'] += float(project.team['main_photographer'].get('salary', 0))
                costs['salaries'] += float(project.team['main_photographer'].get('bonus', 0))

            for member in project.team.get('assist_photographers', []):
                costs['salaries'] += float(member.get('salary', 0))
                costs['salaries'] += float(member.get('bonus', 0))

            for member in project.team.get('makeup_artists', []):
                costs['salaries'] += float(member.get('salary', 0))
                costs['salaries'] += float(member.get('bonus', 0))

            for member in project.team.get('retouch_artists', []):
                costs['salaries'] += float(member.get('salary', 0))
                costs['salaries'] += float(member.get('bonus', 0))

        # Partner costs
        if project.partners:
            costs['partners'] = float(project.partners.get('total_cost', 0))

        total_cost = sum(costs.values())
        profit = revenue - total_cost
        profit_margin = (profit / revenue * 100) if revenue > 0 else 0

        return {
            'project_id': str(project.id),
            'project_code': project.project_code,
            'customer_name': project.customer_name,
            'revenue': revenue,
            'costs': costs,
            'total_cost': total_cost,
            'profit': profit,
            'profit_margin': profit_margin
        }

    @staticmethod
    def cash_flow(month: str) -> Dict:
        """
        Dòng tiền tháng.

        Args:
            month: Tháng (YYYY-MM)

        Returns:
            Dict chứa thông tin dòng tiền
        """
        year, month_num = map(int, month.split('-'))

        # Get projects in month
        projects = Project.objects.filter(
            shoot_date__year=year,
            shoot_date__month=month_num
        )

        # Calculate inflow (payments received)
        total_inflow = 0
        for project in projects:
            if project.payment and 'paid' in project.payment:
                total_inflow += float(project.payment['paid'])

        # Calculate outflow (salaries + partner costs)
        salary_outflow = MonthlySalary.objects.filter(
            month=month,
            is_paid=True
        ).aggregate(total=Sum('total_salary'))['total'] or 0

        partner_outflow = 0
        for project in projects:
            if project.partners:
                partner_outflow += float(project.partners.get('total_cost', 0))

        total_outflow = float(salary_outflow) + partner_outflow

        return {
            'period': month,
            'opening_balance': 0,  # TODO: Implement balance tracking
            'total_inflow': total_inflow,
            'total_outflow': total_outflow,
            'closing_balance': total_inflow - total_outflow,
            'inflow_details': {
                'project_payments': total_inflow
            },
            'outflow_details': {
                'salaries': float(salary_outflow),
                'partners': partner_outflow
            }
        }

    @staticmethod
    def revenue_by_package(month: str) -> Dict:
        """
        Doanh thu theo gói chụp.

        Args:
            month: Tháng (YYYY-MM)

        Returns:
            Dict chứa doanh thu theo gói
        """
        year, month_num = map(int, month.split('-'))

        projects = Project.objects.filter(
            shoot_date__year=year,
            shoot_date__month=month_num
        ).select_related('package_type')

        package_revenue = {}
        total_revenue = 0

        for project in projects:
            package_name = project.package_name
            revenue = float(project.package_final_price)

            if package_name not in package_revenue:
                package_revenue[package_name] = {
                    'package_name': package_name,
                    'project_count': 0,
                    'revenue': 0
                }

            package_revenue[package_name]['project_count'] += 1
            package_revenue[package_name]['revenue'] += revenue
            total_revenue += revenue

        return {
            'period': month,
            'packages': list(package_revenue.values()),
            'total_revenue': total_revenue
        }

    @staticmethod
    def financial_summary(month: str) -> Dict:
        """
        Tổng hợp tài chính.

        Args:
            month: Tháng (YYYY-MM)

        Returns:
            Dict chứa tổng hợp tài chính
        """
        overview = FinanceService.monthly_overview(month)

        # Calculate pending payments
        year, month_num = map(int, month.split('-'))
        projects = Project.objects.filter(
            shoot_date__year=year,
            shoot_date__month=month_num
        )

        pending_payments = 0
        for project in projects:
            if project.payment and 'paid' in project.payment:
                paid = float(project.payment['paid'])
                total = float(project.package_final_price)
                pending_payments += (total - paid)

        return {
            'period': month,
            'revenue': overview['total_revenue'],
            'costs': overview['total_costs'],
            'profit': overview['total_profit'],
            'profit_margin': (overview['total_profit'] / overview['total_revenue'] * 100) if overview['total_revenue'] > 0 else 0,
            'project_count': overview['project_count'],
            'completed_projects': overview['completed_project_count'],
            'pending_payments': pending_payments,
            'total_salaries': overview['cost_breakdown']['salaries'],
            'partner_costs': overview['cost_breakdown']['partners']
        }
