<?php

namespace Tests\Unit;

use App\Http\Controllers\HomeController;
use App\Models\Cart;
use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Http\Request, RedirectResponse;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Testing\Assert;
use Tests\TestCase;
use PDF;

class HomeControllerTest extends TestCase
{
    use DatabaseTransactions;
    protected $cus = 'congdanhabc@outlook.com.vn';
    protected $admin = 'ncongdanh91@gmail.com';
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

    public function test_home_index()
    {
        $user = $this->authenticate($this->cus);
        // Đếm cart_amount từ database
        $cartAmount = Cart::where('user_id', $user->id)
                               ->where('product_order', 'no')
                               ->count();

        $controller = new HomeController();
        $response = $controller->index();
        $view_name = $response->name();
        $view_cart_amount = $response->getData()['cart_amount'];
        dump("View's name is: ". $view_name);
        dump("Cart amount expected-actual: ".$cartAmount."-".$view_cart_amount);
        $this->assertInstanceOf(\Illuminate\View\View::class, $response);
        $this->assertEquals('home', $view_name);
        $this->assertEquals($cartAmount, $view_cart_amount);
    }

    public function test_redirects_guest()
    {
        $controller = new HomeController();
        $response = $controller->redirects();
        $this->assertEquals(url('/login'),$response->getTargetUrl());
    }

    public function test_redirects_cus()
    {
        $user = $this->authenticate($this->cus);
        // Đếm cart_amount từ database
        $cartAmount = Cart::where('user_id', $user->id)
                               ->where('product_order', 'no')
                               ->count();

        $controller = new HomeController();
        $response = $controller->redirects();
        $view_name = $response->name();
        $view_cart_amount = $response->getData()['cart_amount'];
        dump("View's name is: ". $view_name);
        dump("Cart amount expected-actual: ".$cartAmount."-".$view_cart_amount);
        $this->assertInstanceOf(\Illuminate\View\View::class, $response);
        $this->assertEquals('home', $view_name);
        $this->assertEquals($cartAmount, $view_cart_amount);
    }

    public function test_redirects_admin()
    {
        $user = $this->authenticate($this->admin);

        $controller = new HomeController();
        $response = $controller->redirects();
        $view_name = $response->name();
        dump("View's name is: ". $view_name);
        $this->assertInstanceOf(\Illuminate\View\View::class, $response);
        $this->assertEquals('admin.dashboard', $view_name);
    }
}
// ./vendor/bin/phpunit tests/Unit/HomeControllerTest.php --filter test_redirects_admin
