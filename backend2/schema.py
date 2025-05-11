import graphene
from graphene_django import DjangoObjectType
from customers.models.customer import Customer
from customers.models.order import Order
from customers.models.employee import Employee

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = '__all__'

class EmployeeType(DjangoObjectType):
    class Meta:
        model = Employee
        fields = '__all__'

class ItemType(DjangoObjectType):
    class Meta:
        model = Employee
        fields = '__all__'
              
class CreateOrder(graphene.Mutation):
    class Arguments:
        description = graphene.String()
        total_in_cents = graphene.Int()
        customer = graphene.ID()

    order = graphene.Field(OrderType)

    def mutate(root, info, description, total_in_cents, customer):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        try:
            c = Customer.objects.get(pk=customer, user=user) #ensure customer belongs to user
            order = Order(description=description, total_in_cents=total_in_cents, customer=c)
            order.save()
            return CreateOrder(order=order)
        except Customer.DoesNotExist:
            raise Exception("Invalid customer ID or unauthorized")
        
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        industry = graphene.String()
    
    customer = graphene.Field(CustomerType)

    def mutate(root, info, name, industry):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        
        customer = Customer(name=name, industry=industry, user=user)
        customer.save()
        return CreateCustomer(customer=customer)

class CreateEmployee(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID()
        full_name = graphene.String()
        role = graphene.String()
        image = graphene.String()
    
    employee = graphene.Field(EmployeeType)
    
    def mutate(root, info, uuid, full_name, role, image):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        
        employee = Employee(uuid=uuid, full_name=full_name, role=role, user=user, image=image)
        employee.save()
        return CreateEmployee(employee=employee)
    
# custom graphql query
class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    orders = graphene.List(OrderType)
    employees = graphene.List(EmployeeType)
    customer_by_name = graphene.List(CustomerType, name=graphene.String(required=True))

    def resolve_customers(root, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        return Customer.objects.filter(user=user)
    
    def resolve_orders(root, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        return Order.objects.filter(customer__user=user).select_related('customer')
    
    def resolve_employees(root, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        return Employee.objects.filter(user=user)
      
    def resolve_customer_by_name(root, info, name):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        return Customer.objects.filter(name=name, user=user)

class Mutations(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    create_order = CreateOrder.Field()
    create_employee = CreateEmployee.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)