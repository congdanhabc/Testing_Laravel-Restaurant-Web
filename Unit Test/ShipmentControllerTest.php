<?php

namespace Tests\Unit;

use App\Models\Cart;
use Illuminate\Foundation\Testing\DatabaseTransactions;
use Tests\TestCase;
use App\Models\User;
use App\Models\order;

class ShipmentControllerTest extends TestCase
{
    use DatabaseTransactions;
    protected $cus = 'congdanhabc@outlook.com.vn';
    protected $cartAmount;
    protected function authenticate($email_user)
    {
        $user = User::where('email', $email_user)->first();
        if (!$user) {
            $this->markTestSkipped('User not found for testing.');
        }

        $this->actingAs($user);
        return $user;
    }

    public function test_confirm_place_order()
    {
        $user = $this->authenticate($this->cus);
        $cartCount = Cart::where('user_id', $user->id)->count();
        dump("Items in Cart: ". $cartCount);
        $response1 = $this->get(route('cart'));
        $total_price = $response1->viewData('total_price') + $response1->viewData('total_extra_charge');

        $response2 = $this->postJson(route('confirm_place_order', ['total' => $total_price]), ['address' => 'Test Address',]);
        $response2->assertViewIs('Confirm_order');
        $invoice = $response2->viewData('invoice');
        $actual_total = $response2->viewData('total');
        dump("Invoice: ". $invoice);
        dump("Total price expected-actual: ". $total_price."-". $actual_total);
        $this->assertEquals($total_price, $actual_total);
        $this->assertDatabaseHas('carts', [
            'invoice_no' => $invoice,
        ]);
    }

    public function test_trace_order()
    {
        $user = $this->authenticate($this->cus);
        $response1 = $this->get(route('cart'));
        $total_price = $response1->viewData('total_price') + $response1->viewData('total_extra_charge');
        $response2 = $this->postJson(route('confirm_place_order', ['total' => $total_price]), ['address' => 'Test Address',]);
        $invoice = $response2->viewData('invoice');
        $response3 = $this->postJson(route('trace.confirm'), ['phone' => $user->phone, 'invoice' => $invoice,]);
        $response3->assertViewIs('trace_confirm');
        $actual_total = $response3->viewData('total_price');
        dump("Total price expected-actual: ". $total_price."-". $actual_total);
        $this->assertEquals($total_price, $actual_total);
    }

    public function test_trace_order_wrong()
    {
        $user = $this->authenticate($this->cus);
        $response1 = $this->get(route('cart'));
        $total_price = $response1->viewData('total_price') + $response1->viewData('total_extra_charge');
        $response2 = $this->postJson(route('confirm_place_order', ['total' => $total_price]), ['address' => 'Test Address',]);
        $invoice = $response2->viewData('invoice');
        $response3 = $this->postJson(route('trace.confirm'), ['phone' => $user->phone, 'invoice' => 'wrong',]);
        $response3->assertSessionHas('wrong', 'Invaild Invoice no !');
        $response4 = $this->postJson(route('trace.confirm'), ['phone' => '000000', 'invoice' => $invoice,]);
        $response4->assertSessionHas('wrong', 'Wrong phone no !');
    }
}
//./vendor/bin/phpunit tests/Unit/ShipmentControllerTest.php --filter test_trace_order_wrong
